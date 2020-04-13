from flask import Flask, jsonify, request, render_template, abort, Response
import json
#import flask_restful
import re
import pymongo
import requests
from datetime import datetime
import time
# from pymongo import MongoClient

#WORKING  WITH THE DATABASE

myclient = pymongo.MongoClient("mongodb://user_mongodb:27017/")
mydb = myclient["RideShare_users"]
users = mydb["users"]
count = mydb["count"]

app = Flask(__name__)

def increment_count():
    found = 0
    dbquery = count.find({})
    for i in dbquery:
        found = 1
        break
    if found == 0:
        query = {"id" : "counting_accesses", "access" : 0}
        count.insert(query)
    else:
        value = 0
        select = {"id" : "counting_accesses"}
        dbquery = count.find(select)
        for i in dbquery:
            value = i["access"]
            break
        value += 1
        new_value = {"$set" : {"access" : value}}
        count.update(select, new_value)
    return 0

@app.errorhandler(404)
def not_found_error(error):
    return "Not found", 404

@app.errorhandler(400)
def bad_request_error(error):
    return "Bad Request", 400

@app.errorhandler(405)
def method_not_allowed_error(error):
    return "Methods Not Allowed", 405

@app.errorhandler(500)
def internal_server_error(error):
    return "Internal Server Error", 500

#API'S

@app.route('/')
def test():
    return "HELLO WORLD"

@app.route('/api/v1/users', methods = ['PUT'])
def add_user():
    if (request.method == 'PUT'):
        increment_count()
        dataDict = request.get_json()
        password = dataDict["password"]
        pattern = re.compile(r'\b[0-9a-f]{40}\b')
        match = re.match(pattern, password)
        if ( match == None):
            return {}, 400    #PASSWORD NOT IN THE CORRECT FORMAT
        else:
            d = {}
            d["table"] = "users"
            d["work"] = "INSERT"
            d["data"] = dataDict
            d["check"] = "user"
            found = requests.post("http://localhost:8080/api/v1/db/read", data = json.dumps(d))
            found = found.text
            found = int(found)
            if (found == 1):
                return {}, 400  #username already exists
            else:
                retjson = requests.post("http://localhost:8080/api/v1/db/write", data = json.dumps(d))
                return {}, 201  #successfully inserted
    else:
        return {}, 405   #IF METHOD USED IS NOT PUT


@app.route('/api/v1/users/<username>', methods = ['DELETE'])
def remove_user(username):
    if (request.method == 'DELETE'):
        increment_count()
        dataDict = {"username" : username}
        d = {}
        d["table"] = "users"
        d["work"] = "DELETE"
        d["data"] = dataDict
        d["check"] = "user"
        found = requests.post("http://localhost:8080/api/v1/db/read", data = json.dumps(d))
        found = found.text
        found = int(found)
        if (found == 0):
            return {}, 400    #USERNAME NOT FOUND
        else:
            retjson = requests.post("http://localhost:8080/api/v1/db/write", data = json.dumps(d))
            return {}, 200
    else:
        return {}, 405 #IF THE METHOD USED IS NOT DELETE

@app.route('/api/v1/users', methods = ['GET'])
def get_all_users():
    if (request.method == 'GET'):
        increment_count()
        d = {}
        d['table'] = "users"
        d["work"] = "GET_ALL"
        d["check"] = None
        d["data"] = {}
        db_query = requests.post("http://localhost:8080/api/v1/db/read", data = json.dumps(d))
        dbquery = json.loads(db_query.text)
        # for i in dbquery:
        return jsonify(dbquery), 200
    else:
        return {}, 405

@app.route('/api/v1/db/read', methods = ['POST'])
def db_read():

    dataDict = json.loads(request.data)
    table = dataDict["table"]
    work = dataDict["work"]
    data = dataDict["data"]
    check = dataDict["check"]
    if table != '' and table != None and work != None and work != '':
        if check == "user":
            username = data["username"]
            search = {"username" : username}
            users = mydb["users"]
            dbquery = users.find(search)
            # print("alpha")
            for i in dbquery:
            #     print("alpha2")
                return "1"
            # print("alpha1")
            return "0"
        
        elif table == "users" and work == "GET_ALL":
            
            users = mydb["users"]
            dbquery = users.find({})
            li = []
            flag = 0
            for i in dbquery:
                flag = 1
                li.append(i['username'])
            return jsonify(li), 200

    else:
        return {}, 400


@app.route('/api/v1/db/write', methods = ['POST'])
def db_write():
    dataDict = json.loads(request.data)
    table = dataDict["table"]
    work = dataDict["work"]
    data = dataDict["data"]
    if table != '' and table != None and work != None and work != '':
        if table == "users" and work == "INSERT":
            username = data["username"]
            password = data["password"]
            users.insert(({"username" : username, "password" : password}))
            return {}, 201

        elif table == "users" and work == "DELETE":
            username = data["username"]
            search = {"username" : username}
            x = users.delete_many(search)
            return "Successfully deleted"

    else:
        return "Bad request", 400


@app.route('/api/v1/db/clear', methods = ["POST"])
def db_clear():
    dblist = myclient.list_database_names()
    if "RideShare_users" in dblist:
        myclient.drop_database('RideShare_users')
        return {}, 200
    else:
        return {}, 400

### ASSIGNMENT 3    ###

@app.route('/api/v1/_count', methods = ["GET", "DELETE"])
def count_requests():
    if (request.method == "GET"):
        query = {"id" : "counting_accesses"}
        dbquery = count.find(query)
        found = 0
        for i in dbquery:
            value = i["access"]
            found = 1
            break
        if found == 0:
            li = [0]
            return jsonify(li), 200
        else:
            li = [value]
            return jsonify(li), 200

    elif (request.method == "DELETE"):
        query = {"id" : "counting_accesses"}
        dbquery = count.find(query)
        found = 0
        for i in dbquery:
            value = i["access"]
            found = 1
            break
        if found == 0:
            return {}, 200
        else:
            select = {"id" : "counting_accesses"}   
            new_value = {"$set" : {"access" : 0}}
            count.update(select, new_value)
            return {}, 200

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 8080, debug=True)
