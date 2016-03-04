from flask import Flask, request, render_template
from werkzeug.serving import run_simple
import pymysql.cursors
import os

import json

app = Flask(__name__, template_folder='templates')

with open("config.json") as config:
    config = json.loads(config.read())


@app.route("/card-try", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/card-reader", methods=["POST"])
def cardReader():
    studentID = request.form["studentID"]
    name = request.form["name"]
    raw = request.form["raw"]

    connection = pymysql.connect(host=config["host"],
                                 user=config["user"],
                                 password=config["password"],
                                 db=config["dbname"],
                                 charset=config["charset"],
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    sql = "INSERT INTO dataList(name, studentID, cardText) VALUES(%s, %s, %s)"
    cursor.execute(sql, (name, studentID, raw))
    cursor.close()
    connection.commit()
    connection.close()

    return ""

if __name__ == "__main__":
    print os.path.abspath(app.template_folder)
    run_simple(config["website"], config["port"], app,
               use_reloader=True, use_debugger=True, use_evalex=True)
