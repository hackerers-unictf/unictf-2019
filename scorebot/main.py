#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json, random, logging, datetime
import time, sys, bcrypt, timeout_decorator, threading

from pwn import remote

from paramiko import SSHClient
# from scp import SCPClient

from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask, request, Response
from flask_cors import CORS

from joblib import Parallel, delayed

from pprint import pprint
from getpass import getpass

from utils import *

app = Flask(__name__)
CORS(app)

app.url_map.strict_slashes = False

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('MASHDEPIXEL - SCOREBOT')

logging.getLogger("paramiko").setLevel(logging.WARNING)

mongodb = MongoClient( )[ "unict-ctf" ]
current_game = None
services = {
    "cracckami": {
        "port": 1234,
        "flagpath": "/home/alessandro/cracckamiflag.txt"
    },
    "bellosei": {
        "port": 3456,
        "flagpath": "/home/alessandro/belloseiflag.txt"
    },
    "easybof": {
        "port": 4567,
        "flagpath": "/home/alessandro/Downloads/BOF_EASY/arinzaadm"
    }
}

SALT = b"$2b$12$m76fLc4PgIfXfK0dUc0pCu"

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

def put_flag(host, servicename, flag):
    service = services[ servicename ]
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
    stdin, stdout, stderr = ssh.exec_command("echo -n {} > {}".format(flag, service['flagpath']))
    """
    with SCPClient(ssh.get_transport()) as scp:
        scp.put('flag.txt', 'toserver.txt')
    """

def get_flag(host, servicename, flag):
    service = services[ servicename ]
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(host['ipaddress'], username=host['username'], password=host['password'])
    stdin, stdout, stderr = ssh.exec_command("cat {}".format(service['flagpath']))
    flag = stdout.readlines()
    return flag

# Exception raise after timeout
@timeout_decorator.timeout(30, use_signals=False)
def service_is_up( host, service ):
    try:
        connection = remote(host, service['port'])
        connection.recvline()
        connection.close()
        return True
    except Exception as e:
        logger.error("Error with service: {}:{} : {}".format(host, service['port'], e))
        return False
    return False

def updateflag(team, servicename):
    flag =  "unictf{" + ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)]) + '}' # Create the flag
    print("{} {} {}".format(team['host']['ipaddress'], servicename, flag))
    put_flag(team['host'], servicename, flag) # Write flag to file
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
    team = get_team_byname(game['teams'], teamname)
    if game['flags'][ teamname ][ servicename ]['stoled'] is False:
        try:
            if service_is_up( team['host']['ipaddress'], services[ servicename ] ) is True: # Check if service is up
                if safe_str_cmp ( get_flag( team['host']['ipaddress'], services[ servicename ] ), game['flags'][ teamname ][ servicename ]['flag'] ) is True: # Check if flag is integry
                    # Save to database
                    mongodb.ctfgame.update_one({
                        "_id": current_game['_id'],
                        "teams": { "$elemMatch": { "name": teamname } }
                    },
                        { "$inc": { "teams.$.points.defense": 1 } }
                    )
        except Exception as e:
            logger.error("Exception raised on: {}".format(e))

def defensepoint():
    game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, {"flags": 1, "teams": 1} )
    for teamname in game['flags']:
        team = get_team_byname(current_game['teams'], teamname)
        Parallel(n_jobs=4, backend="threading")(delayed(update_defense_point)(game, teamname, servicename) for servicename in game['flags'][ teamname ])

@app.route('/submitflag', methods=['POST'])
def submitflag():
    json_data = request.get_json()

    for field in [ 'flag' , 'teamname' , 'servicename' , 'stoledfrom' ]:
        return Response(json.dumps( {"message": "Please enter a valid: {}".format(field)}), status=400, mimetype='application/json')

    flag_stoled = json_data['flag']
    teamname = json_data['teamname'].lower()
    servicename = json_data['servicename'].lower()
    stoled_from = json_data['stoledfrom'].lower()

    team_attack = get_team_byaddress(current_game['teams'], teamname)
    if team_attack is None:
        return Response(json.dumps( {"message": "{} team not found/valid".format(teamname)}), status=400, mimetype='application/json')

    team_defense = get_team_byaddress(current_game['teams'], stoled_from)
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
            return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "valid"}), status=200, mimetype='application/json')
        else:
            return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "wrong"}), status=400, mimetype='application/json')
    else:
        return Response(json.dumps( {"flag": flag_stoled, "servicename": servicename, "status": "expired"}), status=400, mimetype='application/json')

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
            teamname = input("Name: ").strip()
            game['teams'].append({
                "name": teamname,
                "host": {
                    "ipaddress": input("IP-Address: ").strip(),
                    "username": input("SSH-User: ").lower().strip(),
                    "password": getpass("SSH-Password: ").strip()
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
