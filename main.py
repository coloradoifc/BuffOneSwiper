from flask import Flask
from flask import request
import pymysql.cursors

import json

app = Flask(__name__)

with open("config.json") as config:
    config = json.loads(config.read())

try:
    with open("index.html") as indexPage:
        indexPage = indexPage.read()
except:
    indexPage = "Error cannot find index.html"


@app.route("/card-try", methods=["GET"])
def index():
    return indexPage


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

if __name__ == "__main__":
    app.run()
