#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, json, random, logging, datetime, sys, bcrypt

from pymongo import MongoClient
from bson.objectid import ObjectId

from flask import Flask, request, Response
from flask_cors import CORS

from threading import Thread

from werkzeug.security import safe_str_cmp

from pprint import pprint

app = Flask(__name__)
CORS(app)

app.url_map.strict_slashes = False

# hashed = bcrypt.hashpw(data['password'].encode('utf-8'), SALT)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - [%(funcName)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('MASHDEPIXEL - SCOREBOT')

mongodb = MongoClient( )[ "unict-ctf" ]
current_game = None

SALT = "Tzsx6FBURa" # Change before start the game

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

def updateflag():
    # How to save the flag in the service?
    servicename = ""
    host = ""
    flag = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)])
    flagid = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)])
    mongodb.update_one({ "_id": current_game['_id'], {"$set": { "flags.{}".format(flagid) : {
        "service": servicename,
        "host": host,
        "flag": flag,
        "stoled": False
    } }} })

def defensepoint():
    game = mongodb.find_one({"_id": current_game['_id']}, {"flags": 1} )
    notstoled = [ f for f in game['flags'] if f['stoled'] is False ]
    # Init new defense point to 0 for all teams
    teams = {}
    for team in game['teams']:
        teams[team['host']] = 0
    # Increase defense point if the flags wasn't stoled
    for flag in notstoled:
        teams[flag['host']] += 1
    # Save to database
    for host in teams:
        mongodb.update_one(
            {
                "_id": current_game['_id'],
                "teams": { "$elemMatch": { "name": "host": host } }
            },
            { "$inc": { "teams.$.points.attack": teams[host], } }
        )

def get_team(host):
    for team in current_game['teams']:
        if team['host'] == host:
            return team

@app.route('/submitflag', methods=['POST'])
def submitflag():
    json_data = request.get_json()
    flagid = json_data['flagid']
    team = get_team(request.remote_addr)

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
            "flags": []
        }

        teams_number = input("Insert the number of the teams: ")
        for index in range(0, int(teams_number)):
            print("Team: {}".format( index+1 ))
            game['teams'].append({
                "name": input("Name: "),
                "host": input("IP-Address: "),
                "points": {
                    "attack": 0,
                    "defense": 0
                }
            })
        mongodb.ctfgame.insert_one(game)
    elif int(command) == 1:
        games = list( mongodb.ctfgame.find({}) )
        message = ""
        for index in range(0, len(games)):
            message += "[{}] Game: {}, Start at: {}, Teams: {}\n".format(index, games[index]['name'], games[index]['startdate'], [ t['name'] for t in games[index]['teams'] ] )
        choose = input("Select one of the game:\n{}".format(message))
        game = games[int(choose)]

    current_game = game
    app.run(host='0.0.0.0', port=4526, threaded=True, debug=False)
