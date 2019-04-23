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
    data = json.dumps({"query":"SELECT * FROM users", "username":"ednein"})
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
        return redirect(url_for('query'))
    return redirect(url_for('login'))
    print(session)



@app.route("/query", methods=['GET','POST'])
def query():
    if request.method == "GET":
        if session['username']:
    #     contents = urllib.request.urlopen("http://209.2.226.238:4003/schema").read()
    #     print(contents)
    #     return render_template('index.html', msg = contents)
            return render_template('index.html',username = session['username'])

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if valid_user(username,password):
            session['username'] = username
            return redirect(url_for('query'))
        print("Incorrect")
        return  render_template('login.html',err = "Incorrect username or password")
    return render_template('login.html')

@app.route("/logout")
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/GetData", methods=['GET','POST'])
def GetData():
    columns = request.form.get("columns")
    table = request.form.get("table")
    condition = request.form.get("condition")
    username = session['username']
    print(columns)
    print(table)
    print(condition)
    query = "select "+ columns + " from " + table + " where " + condition
    body = {
        "query": query,
        "username": username
    }

    query_url = "http://localhost:4003/query"
    print("query_url",query_url)
    req = urllib.request.Request(query_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = json.dumps(body)
    data = data.encode('utf-8')
    req.add_header('Content-Length', len(data))
    response = urllib.request.urlopen(req, data)
    result = response.read().decode('utf-8')
    #print(type(result))
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0')
