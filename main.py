import bcrypt
import pymysql.cursors
import json
import os
import sys
from flask import Flask, request, session, redirect, render_template
from flask_api import status
from werkzeug.serving import run_simple
from datetime import timezone, datetime


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# open up the config file
with open("config.json") as config:
    config = json.loads(config.read())

app = Flask(__name__, template_folder='templates')
app.debug = config["debug"]
app.secret_key = config["session-secret"]


# check if the user is logged in
def isLoggedin():
    try:
        if session["loggedin"] == True:
            return True
        else:
            return False

    # this happens if session["loggedin"] is undefined
    except:
        return False


# create the vars that we use for the sessions
def createSession(userID, chapterID):
    session["loggedin"] = True
    session["userID"] = userID
    session["chapterID"] = chapterID


# wrapper to create DB connections
def createDBConnection():
    return pymysql.connect(host=config["host"],
                           user=config["user"],
                           password=config["password"],
                           db=config["dbname"],
                           charset=config["charset"],
                           cursorclass=pymysql.cursors.DictCursor)


# wraper to hash passwords
def hashPassword(passwrd):
    return bcrypt.hashpw(passwrd.encode(), bcrypt.gensalt())

# wraper to check hashed passwords, returns a bool


def checkPassword(passwrd, hashedPass):
    return hashedPass.encode() == bcrypt.hashpw(passwrd.encode(),
                                                hashedPass.encode())


@app.route("/", methods=["GET"])
def index():
    if isLoggedin():

        connection = createDBConnection()

        cursor = connection.cursor()
        sql = "SELECT users.email, chapters.name FROM users, chapters WHERE " + \
            "users.id=%s AND chapters.id = users.chapterID"
        cursor.execute(sql, (session["userID"]))
        results = cursor.fetchone()

        sql = "SELECT id, name, chapterID FROM events WHERE chapterID = %s " + \
            "ORDER BY time_stamp DESC"
        cursor.execute(sql, (session["chapterID"]))
        event_list = cursor.fetchall()

        try:
            eventID = request.args.get("event_id")

            if eventID == None:
                eventID = event_list[0]["id"]
        except:
            eventID = 0

        for item in event_list:

            if item["id"] == int(eventID):
                item["selected"] = True
            else:
                item["selected"] = False
            print(item)

        sql = "SELECT name, studentID, time_stamp FROM dataList WHERE " + \
            "chapterID = %s AND eventID = %s ORDER BY time_stamp DESC"
        cursor.execute(sql, (session["chapterID"], eventID))
        dataList = cursor.fetchall()

        for item in dataList:

            item["time_stamp"] = item[
                "time_stamp"].strftime("%I:%M %p %m/%d/%Y ")

            sql = "SELECT chapters.id, chapters.short_name FROM chapters INNER JOIN " + \
                "blacklist ON blacklist.chapterID = chapters.id WHERE " + \
                "studentID=%s AND blacklisted=1"

            cursor.execute(sql, (item["studentID"]))
            blacklist_names = cursor.fetchall()

            blacklist_names_string = ""
            item["self_blacklisted"] = False
            item["blacklisted"] = False

            for bl_item in blacklist_names:

                item["blacklisted"] = True
                if bl_item["id"] == session["chapterID"]:

                    item["self_blacklisted"] = True

                    blacklist_names_string = bl_item[
                        "short_name"] + blacklist_names_string
                else:
                    blacklist_names_string += "/" + bl_item["short_name"]

            try:
                if blacklist_names_string[0] == "/":
                    blacklist_names_string = blacklist_names_string[1:]
            except:
                pass
            item["blacklist"] = blacklist_names_string

        cursor.close()
        connection.close()

        return render_template('index.html', chapter=results["name"],
                               email=results["email"], dataList=dataList,
                               event_list=event_list, eventID=eventID)
    else:
        return render_template('login.html')


@app.route("/add_event", methods=["POST"])
def createEvent():

    connection = createDBConnection()

    name = request.form["event_name"]
    chapterID = session["chapterID"]

    cursor = connection.cursor()
    sql = "INSERT INTO events(name, chapterID) VALUES(%s, %s)"
    cursor.execute(sql, (name, chapterID))

    cursor.execute("SELECT LAST_INSERT_ID()")
    new_id = cursor.fetchone()["LAST_INSERT_ID()"]

    cursor.close()
    connection.commit()
    connection.close()

    returnDic = {"name": name, "url": new_id}

    return json.dumps(returnDic), status.HTTP_202_ACCEPTED


@app.route("/get_event", methods=["GET"])
def getEvent():

    event_id = request.args.get("event_id")

    connection = createDBConnection()

    cursor = connection.cursor()
    sql = "SELECT name, time_stamp FROM dataList WHERE eventID=%s AND chapterID=%s"
    cursor.execute(sql, (event_id, session["chapterID"]))
    dataList = cursor.fetchall()

    cursor.close()
    connection.close()

    for item in dataList:
        item["time_stamp"] = item[
            "time_stamp"].strftime("%I:%M %p %m/%d/%Y ")

    return json.dumps(dataList), status.HTTP_202_ACCEPTED


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    connection = createDBConnection()

    cursor = connection.cursor()
    sql = "SELECT id, password, chapterID FROM users WHERE email=%s"
    cursor.execute(sql, (email))
    results = cursor.fetchone()

    cursor.close()
    connection.close()

    validCredentials = False

    try:
        if checkPassword(password, results["password"]):
            validCredentials = True
            createSession(results["id"], results["chapterID"])
    except:
        pass

    if validCredentials:
        return "", status.HTTP_202_ACCEPTED
    else:
        return "", status.HTTP_401_UNAUTHORIZED


@app.route("/logout", methods=["GET"])
def removeSession():
    session["loggedin"] = False
    session.clear()
    return redirect("/", code=303)


@app.route("/blacklist", methods=["POST"])
def blacklist():

    studentID = request.form["studentID"]
    adminPassword = request.form["password"]
    shouldBlacklist = bool(request.form["shouldBlacklist"])

    connection = createDBConnection()
    cursor = connection.cursor()

    sql = "SELECT password FROM users WHERE id=%s"
    cursor.execute(sql, (session["userID"]))
    dbPassword = cursor.fetchone()["password"]

    if not checkPassword(adminPassword, dbPassword):
        return "", status.HTTP_401_UNAUTHORIZED

    if shouldBlacklist == True:

        sql = "INSERT INTO blacklist(studentID, chapterID) VALUES(%s, %s) " + \
            " ON DUPLICATE KEY UPDATE blacklisted = 1"
        cursor.execute(sql, (studentID, session["chapterID"]))
    else:
        sql = "UPDATE blacklist SET blacklisted = 0 WHERE studentID = %s AND chapterID = %s"
        cursor.execute(sql, (studentID, session["chapterID"]))

    cursor.close()
    connection.commit()
    connection.close()

    return "", status.HTTP_202_ACCEPTED


@app.route("/card-reader", methods=["POST"])
def cardReader():
    if isLoggedin() == False:
        return "", status.HTTP_401_UNAUTHORIZED

    try:
        studentID = request.form["studentID"]
        name = request.form["name"]
        raw = request.form["raw"]
        eventID = request.form["eventID"]
    except:
        return "", status.HTTP_400_BAD_REQUEST

    userID = session["userID"]
    chapterID = session["chapterID"]

    connection = createDBConnection()

    cursor = connection.cursor()
    sql = "INSERT INTO dataList(name, studentID, card_text, userID, " + \
        "chapterID, eventID) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, studentID, raw, userID, chapterID, eventID))
    cursor.close()
    connection.commit()
    connection.close()

    returnDic = {"name": name, "time": datetime.now(
    ).strftime("%I:%M %p %m/%d/%Y "), "blackList": ["No"]}

    return json.dumps(returnDic), status.HTTP_202_ACCEPTED


# reload the templates without restarting
extra_dirs = ['templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

if __name__ == "__main__":
    run_simple(config["website"], config["port"], app,
               use_reloader=True, use_debugger=True, use_evalex=True,
               extra_files=extra_files)
