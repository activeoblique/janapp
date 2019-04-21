from flask import Flask, request, session, escape, redirect, url_for, send_file, send_from_directory, render_template, make_response
app = Flask(__name__)
import sys
import urllib.request
import json
app.secret_key = b'19960223'
#check whether it is a valid user
def valid_user(username,password):
    #connect to jana and check
    myurl = "http://localhost:4003/query"
    req = urllib.request.Request(myurl)
    data = json.dumps({"query":"SELECT * FROM users", "username":"jana"})
    print(data)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = data.encode('utf8')
    response = json.loads(urllib.request.urlopen(req, data).read().decode('utf8'))
    for user in response['rows']:
        print(user[0])
        if user[0] == username and user[1] == password:
            return True
    return False
@app.route("/", methods=['GET','POST'])
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'
    print(session)
    if request.method == "POST":
        return render_template('index.html')
    return render_template('login.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if valid_user(username,password):
            session['username'] = username
            return render_template('index.html')
        print("Incorrect")
        return  render_template('login.html',err = "Incorrect username or password")
    return render_template('login.html')


# @app.route("/index", methods=['GET','POST'])
# def index():
#     if request.method == "POST":
#         contents = urllib.request.urlopen("http://localhost:4003/schema").read()
#         return render_template('index.html', msg = contents)
#     return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')