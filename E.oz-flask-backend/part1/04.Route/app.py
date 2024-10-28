from flask import Flask, request, Response


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, This is Main page!"

@app.route('/about')
def about():
    return "This is about page!"

@app.route('/company')
def company():
    return "This is company page!"

@app.route('/user/<username>')
def user_profile(username):

    return f'UserName : {username}'

@app.route('/number/<int:number>')
def number(number):

    return f'Number : {number}'

import requests
@app.route('/test')
def test():
    url = 'http://127.0.0.1:5000/submit'
    data = 'test data'
    response = requests.post(url=url, data=data)

    return response

@app.route('/submit', methods=['GET', 'POST', 'PUT', 'DELETE'])
def submit():
    print(request.method)

    if request.method == 'GET':
        print("GET method")

    if request.method == 'POST':
        print("***POST method***", request.data)

    return Response("Successfully submitted", status=200)

if __name__ == "__main__":
    print("__name__ : ", __name__)
    app.run()