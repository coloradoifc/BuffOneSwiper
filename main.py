from flask import Flask, request, session, redirect, render_template
from flask.ext.api import status
from werkzeug.serving import run_simple
import bcrypt
import pymysql.cursors
import json


# open up the config file
with open("config.json") as config:
    config = json.loads(config.read())

app = Flask(__name__, template_folder='templates')
app.debug = config["debug"]
app.secret_key = config["session-secret"]

# get the index page
try:
    with open("index.html") as indexPage:
        indexPage = indexPage.read()
except:
    indexPage = "Error cannot find index.html"

# get the login page
try:
    with open("login.html") as loginPage:
        loginPage = loginPage.read()
except:
    loginPage = "Error cannot find login.html"


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
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    connection = createDBConnection()

    cursor = connection.cursor()
    sql = "SELECT id, password, chapterID FROM users WHERE email=%s"
    cursor.execute(sql, (email))
    results = cursor.fetchone()

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

@app.route("/card-reader", methods=["POST"])
def cardReader():

    if isLoggedin() == False:
        return "", status.HTTP_401_UNAUTHORIZED

    try:
        studentID = request.form["studentID"]
        name = request.form["name"]
        raw = request.form["raw"]
    except:
        return "", status.HTTP_400_BAD_REQUEST

    userID = session["userID"]
    chapterID = session["chapterID"]

    connection = createDBConnection()

    cursor = connection.cursor()
    sql = "INSERT INTO dataList(name, studentID, cardText, userID, " + \
        "chapterID) VALUES(%s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, studentID, raw, userID, chapterID))
    cursor.close()
    connection.commit()
    connection.close()

    return "", status.HTTP_202_ACCEPTED

if __name__ == "__main__":
    run_simple(config["website"], config["port"], app,
               use_reloader=True, use_debugger=True, use_evalex=True)
