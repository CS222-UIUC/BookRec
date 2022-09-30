from flask import Flask
from flask import render_template, request, url_for, redirect, session
from flask_mysqldb import MySQL
import json
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.confi['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

@app.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        pwd_input = request.form['password']
        conn = db.connect()
        pwd_query = ''
        db_data = conn.execute(pwd_query)
        conn.close()
        pwd_res = json.dumps([dict(e) for e in db_res.fetchall()]) 
        pwd = (json.loads(pwd_res[1:len(pwd_res)-1]))["Password"]
        if pwd == pwd_input:
            print("Correct Password")
    
    return render_template("login.html")



    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)