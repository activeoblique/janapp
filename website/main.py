from flask import Flask, request, session, escape, redirect, url_for, send_file, send_from_directory, render_template, make_response, abort
app = Flask(__name__)
import sys
import urllib.request
import json
import ast
import random
import string
from flask_wtf.csrf import CSRFProtect, CSRFError
csrf = CSRFProtect(app)
app.config['SERVER_NAME'] = '34.83.198.40:5000'



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

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

@app.route("/", methods=['GET','POST'])
def index():
    if 'username' in session:
        return redirect(url_for('query'))
    return redirect(url_for('login'))

@app.route("/query", methods=['GET','POST'])
def query():
    if request.method == "GET":
        if 'username' in session:
            return render_template('index.html',username = session['username'])
    return redirect(url_for('login'))


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
    columns = str(request.form.get("columns"))
    table = str(request.form.get("table"))
    condition = str(request.form.get("condition"))
    username = session['username']

    query = ""
    check = []
    if table == "accounts":
        colnames = ["*","account_id", "district_id", "frequency", "date", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns or "count" in condition:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "card":
        colnames = ["*","card_id", "disp_id", "type", "issued", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "client":
        colnames = ["*","client_id", "birth_number", "district_id", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "disp":
        colnames = ["*","disp_id", "client_id", "account_id", "type", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "employees":
        colnames = ["*","name", "age", "department", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "loan":
        colnames = ["*","loan_id", "account_id", "date", "amount", "duration", "payments", "status", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "orders":
        colnames = ["*","order_id", "account_id", "bank_to", "account_to", "amount", "k_symbol", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json

    elif table == "trans":
        colnames = ["*","trans_id", "account_id", "date", "type", "operation", "amount", "balance", "k_symbol", "bank", "account", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    elif table == "predictions":
        colnames = ["*","amount", "account_id", "type", "bank_id"]
        if bool([ele for ele in colnames if(ele in columns)]):
            if condition:
                condition = " where " + condition
            if "count" in columns:
                columns = columns.replace("count(","dp_count(0.1,")
            if "count" in condition:
                condition = condition.replace("count(","dp_count(0.1,")
            query = "select "+ columns + " from " + table + condition
        else:
            print("no such column")
            result = {"error":"Invalid column name."}
            result_json = json.dumps(result)
            return result_json
    else:
        result = {"error":"Invalid table name."}
        result_json = json.dumps(result)
        return result_json

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
    result = ast.literal_eval(response.read().decode('utf-8'))
    result.pop("durationMillis")
    result = str(result)
    result_json = json.dumps(result)
    print(result_json)
    file = open('./your_hmp_result.txt', "w")
    file.write(result)
    return result_json

def get_ratio(table,username):
    query = "select count(*) from " + table
    data = json.dumps({"query": "SELECT count(*) FROM " + table +" WHERE bank_id = 1", "username": username})
    print(data)
    query_url = "http://localhost:4003/query"
    print("query_url",query_url)
    req = urllib.request.Request(query_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = data.encode('utf8')
    response = json.loads(urllib.request.urlopen(req, data).read().decode('utf8'))
    try: yours = response['rows'][0][0]
    except:
        yours = 0
    # query whole database using DP_COUNT
    data = json.dumps({"query": "SELECT DP_COUNT(0.1, *) FROM " + table, "username": "jana"})
    print(data)
    print(yours)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    data = data.encode('utf8')
    response = json.loads(urllib.request.urlopen(req, data).read().decode('utf8'))
    try: overall = response['rows'][0][0]
    except:
        overall = 0
    if overall == 0:
        return 0
    return yours / overall

@app.route("/basic_analysis",methods = ['POST'])
def basci_analysis():
    print(session)
    ratio = []
    if 'username' in session:
        result = ""
        username = session['username']

        tables = ['card','accounts','loan','disp']
        for table in tables:
            ratio = get_ratio(table,username)
            result += "Your portion in " + table + " is " + str(ratio) + "\n"
        return render_template('index.html', analysis = result, username = session['username'])
    return "you are not login"

@app.route('/download', methods=['POST'])
def download():
    # change filename for download
    filename = "query_result.txt"
    print("hmp")
    # create response
    response = make_response(send_file("./your_hmp_result.txt"))
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename
    response.mimetype = 'text/csv'
    return response

@app.route('/personal_analysis',methods = ['POST','GET'])
def personal_analysis():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('personal_analysis.html', username=session['username'])
        return redirect(url_for('login'))
    else:
        account_id = request.form['account_id']
        if 'username' in session:
            username = session['username']
            query = "select * from predictions where account_id = " + account_id
            print(username)
            print(query)
            body = {
                "query": query,
                "username": username
            }
            query_url = "http://localhost:4003/query"
            req = urllib.request.Request(query_url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            data = json.dumps(body)
            data = data.encode('utf-8')
            req.add_header('Content-Length', len(data))
            response = urllib.request.urlopen(req, data)
            result = json.loads(response.read().decode('utf-8'))
            msg = 'The next transaction amount will be'  + result['rows'][0][1] +", then next transaction type will be" + result['rows'][0][2] +' .'
            return msg
    return "you are not logged in"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
