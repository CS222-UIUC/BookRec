from mimetypes import init
from django.shortcuts import render
from flask import Flask
from flask import render_template, request, url_for, redirect, session
import json
import sqlalchemy
import os
import pandas as pd

app = Flask(__name__)

userid = ""
user1booklist = []
user2booklist = []

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
            global userid
            userid = username
            return redirect('/index')
        else:
            return redirect('/incorrectpwd')
    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_file = request.files['file1']
        df1, df2 = pd.DataFrame(), pd.DataFrame()
        if upload_file.filename != '':
            upload_file.save(userid + "_" + upload_file.filename)
            df1 = file_to_df(userid + "_" + upload_file.filename, userid)
            global user1booklist
            user1booklist = getNameList(df1)
            print(df1)
        compare_file = request.files['file2']
        if compare_file.filename != '' and upload_file.filename != '':
            compare_file.save(userid + "_" + compare_file.filename)
            df2 = file_to_df(userid + "_" + compare_file.filename, userid)
            global user2booklist
            user2booklist = getNameList(df2)
            print(df2)
        return redirect(url_for('index'))
    return render_template("index.html")
    
@app.route('/correctpwd')
def correctpwd():
    return "correct password"

@app.route('/incorrectpwd')
def incorrectpwd():
    return "incorrect password"

if __name__ == "__main__":
    app.run(debug=True)


def file_to_df(filename, id):
    df = pd.read_csv(
        filename,
        encoding="ISO-8859-1",
        header=0,
        usecols=["ISBN", "My Rating"],
        dtype={"ISBN":"str", "My Rating": "float"}
    )
    df = df.dropna(subset=['ISBN'])
    for i in range(len(df.index)):
        s = len(df.at[i,'ISBN'])
        df.at[i,'ISBN'] = df.at[i,'ISBN'][2:s-1]
        if (df.at[i,"ISBN"] == ''):
            df = df.drop(i)
    for i in df.index:
        if (df.at[i,"My Rating"] == 0.0):
            df = df.drop(i)
    df = df.rename(columns={"ISBN": "isbn", "My Rating": "rating"})
    df["UserID"] = id
    df = df[['UserID', "isbn", "rating"]]
    return df

def getNameList(dataframe):
    df = dataframe[dataframe["rating"] >= 4.0]
    return df["isbn"].tolist()