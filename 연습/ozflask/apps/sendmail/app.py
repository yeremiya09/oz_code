from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, OZ234"

# @app.route("/hello")
# def hello():
# 	  return "Hello Student2"

@app.route("/hello2", methods=["GET"], endpoint="hello_oz2")
def hello2():
     users = {"파머":"www.farmers.com", "오쌤":"www.oz234.com"}
     return render_template("index.html", users = users)
