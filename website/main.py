from flask import Flask, request, redirect, url_for, send_file, send_from_directory, render_template, make_response
app = Flask(__name__)
import sys
import urllib.request
import json

@app.route("/", methods=['GET','POST'])
def login():
    if request.method == "POST":
        return render_template('index.html')
    return render_template('login.html')


@app.route("/index", methods=['GET','POST'])
def index():
    # if request.method == "POST":
    #     contents = urllib.request.urlopen("http://209.2.226.238:4003/schema").read()
    #     print(contents)
    #     return render_template('index.html', msg = contents)
    return render_template('index.html')
    
@app.route("/GetData", methods=['GET','POST'])
def GetData():
    columns = request.form.get("columns")
    table = request.form.get("table")
    condition = request.form.get("condition")
    print(columns)
    print(table)
    print(condition)
    query = "select "+ columns + " from " + table + " where " + condition
    body = {
        "query": query,
        "username": "jana"
    }
    query_url = "http://192.168.1.13:4003/query"
    req = urllib.request.Request(query_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = json.dumps(body)
    data = data.encode('utf-8')
    req.add_header('Content-Length', len(data))
    response = urllib.request.urlopen(req, data)
    result = response.read().decode('utf-8')
    print(type(result))
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0')