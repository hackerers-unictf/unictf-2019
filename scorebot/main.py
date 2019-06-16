#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json, random, logging, datetime, utils
import time, sys, bcrypt, timeout_decorator, threading

from pwn import remote

from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask, request, Response, render_template
from flask_cors import CORS

from joblib import Parallel, delayed

from pprint import pprint
from getpass import getpass

from servicesup import ServicesUP
servicesup = ServicesUP().servicesup

app = Flask(__name__, template_folder='templates', static_folder="static")
CORS(app)

app.url_map.strict_slashes = False

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('MASHDEPIXEL - SCOREBOT')

logging.getLogger("paramiko").setLevel(logging.WARNING)

mongodb = MongoClient( )[ "unict-ctf" ]
current_game = None

with open('services.json') as f:
    services = json.load(f)

SALT = b"$2b$12$m76fLc4PgIfXfK0dUc0pCu" # Change in production

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId) or isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return str(o)
        return json.JSONEncoder.default(self, o)

"""
@app.route('/gameinfo', methods=['GET'])
def gameinfo():
    return Response(json.dumps(current_game, cls=JSONEncoder), status=200, mimetype='application/json')
"""

# Exception raise after timeout
@timeout_decorator.timeout(30, use_signals=False)
def service_is_up( host, servicename ):
    try:
        return servicesup[ servicename ] ( host , services[ servicename ]['port'] )
    except Exception as e:
        logger.error("Error with service: {}:{} : {}".format(host, services[ servicename ]['port'], e))
        return False
    return False

def updateflag(team, servicename):
    flag =  "unictf{" + ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)]) + '}' # Create the flag
    utils.put_flag(team['host'], services[ servicename ], flag) # Write flag to file
    mongodb.ctfgame.update_one({ "_id": current_game['_id'] }, { "$set": {
        "flags.{}.{}".format(team['name'], servicename) : {
            "flag": bcrypt.hashpw(flag.encode('utf-8'), SALT) ,
            "stoled": False,
            "generate_at": datetime.datetime.now()
        }
    } })

def safe_str_cmp(flag, hashed):
    return bcrypt.hashpw(flag.encode('utf-8'), SALT) == hashed

def routine():
    defensepoint() # Assign defense point if the service is up and the flag wans't stoled.
    time.sleep(10)
    renew_flags() # Set the new flag for each team and service
    threading.Timer(60, routine).start() # Call again after x seconds

def renew_flags():
    for team in current_game['teams']:
        Parallel(n_jobs=4, backend="threading")(delayed(updateflag)(team, servicename) for servicename in services)

def update_defense_point(game, teamname, servicename):
    team = utils.get_team_byname(game['teams'], teamname)
    if game['flags'][ teamname ][ servicename ]['stoled'] is False:
        try:
            if service_is_up( team['host'][ 'ipaddress_{}bit'.format( services[servicename]['arch'] ) ], servicename ) is True: # Check if service is up
                if safe_str_cmp ( utils.get_flag( team['host'], services[ servicename ] ), game['flags'][ teamname ][ servicename ]['flag'] ) is True: # Check if flag is integry
                    # Save to database
                    mongodb.ctfgame.update_one({
                        "_id": current_game['_id'],
                        "teams": { "$elemMatch": { "name": teamname } }
                    },
                        { "$inc": { "teams.$.points.defense": 1 } }
                    )
                    utils.append_to_history(mongodb, current_game['_id'], "{} , {} DEFENSE +1!".format( teamname.title(), servicename ) )
                else:
                    utils.append_to_history(mongodb, current_game['_id'], "{} , {} FLAG NOT INTEGRITY".format( teamname.title(), servicename ) )
            else:
                utils.append_to_history(mongodb, current_game['_id'], "{} , {} SERVICE DOWN!".format( teamname.title(), servicename ) )
        except Exception as e:
            logger.error("Exception raised on: {}".format(e))

def defensepoint():
    game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, {"flags": 1, "teams": 1} )
    for teamname in game['flags']:
        team = utils.get_team_byname(current_game['teams'], teamname)
        Parallel(n_jobs=4, backend="threading")(delayed(update_defense_point)(game, teamname, servicename) for servicename in game['flags'][ teamname ])

@app.route("/", methods=['GET'])
def hello():
    game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, { "flags": 0 } )
    game['history'] = game['history'][:10]
    return render_template('index.html', game=game)

@app.route('/submitflag', methods=['GET', 'POST'])
def submitflag():
    if request.method == "GET":
        game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, { "flags": 0 , "history": 0} )
        return render_template('submit.html', game=game, services=services)
    else:
        json_data = request.get_json()
        if json_data is None:
            json_data = request.form.to_dict()
        try:
            for field in [ 'flag' , 'teamname' , 'servicename' , 'stoledfrom' ]:
                if field not in json_data:
                    return Response(json.dumps( {"message": "Please enter a valid: {}".format(field)}), status=400, mimetype='application/json')

            flag_stoled = json_data['flag']
            teamname = json_data['teamname']
            servicename = json_data['servicename'].lower()
            stoled_from = json_data['stoledfrom'].lower()

            team_attack = utils.get_team_byaddress(current_game['teams'], teamname)
            if team_attack is None:
                return Response(json.dumps( {"message": "{} team not found/valid".format(teamname)}), status=400, mimetype='application/json')

            team_defense = utils.get_team_byaddress(current_game['teams'], stoled_from)
            if team_defense is None:
                return Response(json.dumps( {"message": "{} team not found/valid".format(stoled_from)}), status=400, mimetype='application/json')

            if servicename not in services.keys():
                return Response(json.dumps( {"message": "{} service found/valid".format(servicename)}), status=400, mimetype='application/json')

            if team_attack['name'] == team_defense['name']:
                return Response(json.dumps( {"message": "Attack and defense team cannot be the same"}), status=400, mimetype='application/json')

            game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, {"flags": 1} )
            dbflag = game['flags'][ team_defense['name'] ][ servicename ]
            if dbflag['stoled'] is False:
                if safe_str_cmp(flag_stoled, dbflag['flag'] ): # Flags match!
                    mongodb.ctfgame.update_one(
                        {
                            "_id": current_game['_id'],
                            "teams": { "$elemMatch": { "name": team_attack['name'], "host": team_attack['host'] } }
                        },
                        { "$inc": { "teams.$.points.attack": 2, } }
                    )
                    time.sleep(1)
                    mongodb.ctfgame.update_one(
                        {
                            "_id": current_game['_id'],
                        },
                        { "$set": { "flags.{}.{}.stoled".format( team_defense['name'], servicename ): True, } }
                    )
                    utils.append_to_history(mongodb, current_game['_id'], "{} submit a VALID flag! ATTACK +2".format( team_attack['name'].title() ) )
                    return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "valid"}), status=200, mimetype='application/json')
                else:
                    utils.append_to_history(mongodb, current_game['_id'], "{} submit a WRONG flag!".format( team_attack['name'].title() ) )
                    return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "wrong"}), status=400, mimetype='application/json')
            else:
                utils.append_to_history(mongodb, current_game['_id'], "{} submit a EXPIRED flag!".format( team_attack['name'].title() ) )
                return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "expired"}), status=400, mimetype='application/json')
        except Exception as e:
            logger.error("Exception raised with the following args: {}. Exception: {}".format(json_data, e))
            return Response(json.dumps( {"message": "Scorebot Exception"}), status=500, mimetype='application/json')

if __name__ == '__main__':
    command = input("[0] Start new game\n[1] Restore from db\n")
    if int(command) == 0:
        game = {
            "teams": [],
            "name": input("CTF-Name: "),
            "startdate": datetime.datetime.now(),
            "history": [],
            "flags": {}
        }

        teams_number = input("Insert the number of the teams: ")
        for index in range(0, int(teams_number)):
            print("Team: {}".format( index+1 ))
            teamname = input("Name: ").lower().strip()
            game['teams'].append({
                "name": teamname,
                "host": {
                    # "ipaddress": input("IP-Address: ").strip(),
                    "ipaddress_32bit": input("IP-Address 32Bit: ").strip(),
                    "ipaddress_64bit": input("IP-Address 64Bit: ").strip(),
                    "username": input("SSH-User: ").lower().strip()
                    # "sshkeypath": input("SSH-Key: ").lower().strip(), # Load from system
                    # "password": getpass("SSH-Password: ").strip() # RSA Key
                },
                "points": {
                    "attack": 0,
                    "defense": 0
                }
            })
            game['flags'][ teamname ] = {}
        mongodb.ctfgame.insert_one(game)
    elif int(command) == 1:
        games = list( mongodb.ctfgame.find({}) )
        message = ""
        for index in range(0, len(games)):
            message += "[{}] Game: {}, Start at: {}, Teams: {}\n".format(index, games[index]['name'], games[index]['startdate'], [ t['name'] for t in games[index]['teams'] ] )
        choose = input("Select one of the game:\n{}".format(message))
        game = games[int(choose)]

    current_game = game
    threading.Timer(5, routine).start()
    app.run(host='0.0.0.0', port=4526, threaded=True, debug=False)
