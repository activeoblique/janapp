from flask import Flask, request, redirect, url_for, send_file, send_from_directory, render_template, make_response
app = Flask(__name__)
import sys
import urllib.request

@app.route("/", methods=['GET','POST'])
def login():
    if request.method == "POST":
        return render_template('index.html')
    return render_template('login.html')


@app.route("/index", methods=['GET','POST'])
def index():
    if request.method == "POST":
        contents = urllib.request.urlopen("http://129.236.232.252:4003/schema").read()
        return render_template('index.html', msg = contents)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')