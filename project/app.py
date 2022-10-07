from django.shortcuts import render
from flask import Flask
from flask import render_template, request, url_for, redirect, session

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/index')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)