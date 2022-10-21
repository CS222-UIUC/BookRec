from mimetypes import init
from django.shortcuts import render
from flask import Flask
from flask import render_template, request, url_for, redirect, session
import json
import sqlalchemy
import os

app = Flask(__name__)

db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL(
                drivername="mysql+pymysql",
                username= "root",
                password= "Will1419Root",
                database= "CS222Data",
                host= "127.0.0.1"
            )
        )

@app.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd_input = request.form['password']
        conn = db.connect()
        pwd_query = 'SELECT * FROM CS222Data.userinfo WHERE Username="{}"'.format(username) 
        db_res = conn.execute(pwd_query)
        conn.close()
        pwd_res = json.dumps([dict(e) for e in db_res.fetchall()]) 
        pwd = (json.loads(pwd_res[1:len(pwd_res)-1]))["password"] 
        print(pwd)
        if pwd == pwd_input:
            return redirect('/correctpwd')
        else:
            return redirect('/incorrectpwd')
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/correctpwd')
def correctpwd():
    return "correct password"

@app.route('/incorrectpwd')
def incorrectpwd():
    return "incorrect password"

if __name__ == "__main__":
    app.run(debug=True)