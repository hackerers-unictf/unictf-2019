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

from werkzeug.security import safe_str_cmp

from pprint import pprint
from getpass import getpass

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
    }
}

SALT = bcrypt.gensalt(10)

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
    stdin, stdout, stderr = ssh.exec_command("cat filename.txt")
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
    flag =  "CTF_" + ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)]) # Create the flag
    put_flag(team['host'], servicename, flag) # Write flag to file
    mongodb.ctfgame.update_one({ "_id": current_game['_id'] }, { "$set": {
        "flags.{}.{}".format(team['name'], servicename) : {
            "flag": bcrypt.hashpw(flag.encode('utf-8'), SALT) ,
            "stoled": False,
            "generate_at": datetime.datetime.now()
        }
    } })

def routine():
    defensepoint() # Assign defense point if the service is up and the flag wans't stoled.
    renew_flags() # Set the new flag for each team and service
    threading.Timer(60, routine).start() # Call again after x seconds

def renew_flags():
    for team in current_game['teams']:
        Parallel(n_jobs=4, backend="threading")(delayed(updateflag)(team, servicename) for servicename in services)

def defensepoint():
    game = mongodb.ctfgame.find_one({"_id": current_game['_id']}, {"flags": 1} )
    for teamname in game['flags']:
        defense_point = 0
        team = get_team(teamname, 'name')
        # Increase defense point if the flags wasn't stoled
        for servicename in game['flags'][ teamname ]: # DA PARALLELIZZARE!!!
            if game['flags'][ teamname ][ servicename ]['stoled'] is False:
                try:
                    # if service_is_up( team['host']['ipaddress'], services[ servicename ] ) is True: # Check if service is up
                    #     if safe_str_cmp ( get_flag( team['host']['ipaddress'], services[ servicename ] ), game['flags'][ teamname ][ servicename ]['flag'] ) is True: # Check if flag is integry
                    defense_point += 1
                except Exception as e:
                    logger.error("Exception raised on: {}".format(e))
        # Save to database
        mongodb.ctfgame.update_one({
            "_id": current_game['_id'],
            "teams": { "$elemMatch": { "name": teamname } }
        },
            { "$inc": { "teams.$.points.defense": defense_point } }
        )
        logger.info("Assign +{} defense points to {} team!".format(defense_point, teamname))

def get_team(value, field):
    for team in current_game['teams']:
        if team[field] == value:
            return team

@app.route('/submitflag', methods=['POST'])
def submitflag():
    json_data = request.get_json()
    flagid = json_data['flagid']
    team = get_team(request.remote_addr, 'host')

    game = mongodb.find_one({"_id": current_game['_id']}, {"flags": 1} )
    flags = game['flags']
    if safe_str_cmp(json_data['flag'], flags['flagid']['flag']): # Flags match!
            mongodb.update_one(
                {
                    "_id": current_game['_id'],
                    "teams": { "$elemMatch": { "name": team['name'], "host": team['host'] } }
                },
                { "$inc": { "teams.$.points.attack": 2, } }
            )
            mongodb.update_one(
                {
                    "_id": current_game['_id'],
                    "flags": { "$elemMatch": flags['flagid'] }
                },
                { "$set": { "flags.$.stoled": True, } }
            )
            # Remove flagid and set new flag for corresponding service.
    return Response(json.dumps( {"team": team} , cls=JSONEncoder), status=200, mimetype='application/json')

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
