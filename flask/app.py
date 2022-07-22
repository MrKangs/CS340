from flask import Flask, render_template, redirect, url_for
import os
from flask_mysqldb import MySQL
from flask import request
import database.autogenerator as pk_generator

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_kangken'
app.config['MYSQL_PASSWORD'] = '8280' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_kangken'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Variables
pk_userAccounts = 0
pk_fiatWallets = 0
pk_dogecoinWallets = 0
pk_exchangeOrders = 0
pk_dogecoinTransactions = 0
externalWalletID = set()
transactionHash = set()

# Routes

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/userAccountsEntity.html', methods=["POST", "GET"])
def user():
    if request.method == "GET":
        query = "SELECT * FROM userAccounts"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return render_template("userAccountsEntity.html", users=data)

@app.route('/userAccountsForm.html')
def userform():
    return render_template("userAccountsForm.html")

@app.route('/fiatWalletsEntity.html', methods=["POST", "GET"])
def fiatwallet():
    if request.method == "GET":
        query = "SELECT * FROM fiatWallets"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return render_template("fiatWalletsEntity.html", fiatwallets=data)

@app.route('/fiatWalletsForm.html')
def fiatwalletform():
    return render_template("fiatWalletsForm.html")

@app.route('/dogecoinWalletsEntity.html', methods=["POST", "GET"])
def dogecoinwallet():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinWallets"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return render_template("dogecoinWalletsEntity.html", dogecoinWallets=data)

@app.route('/dogecoinWalletsForm.html')
def dogecoinwalletform():
    return render_template("dogecoinWalletsForm.html")

@app.route('/exchangeOrdersEntity.html', methods=["POST", "GET"])
def exchangeorder():
    if request.method == "GET":
        query = "SELECT * FROM exchangeOrders"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return render_template("exchangeOrdersEntity.html", exchangeOrders=data)

@app.route('/exchangeOrdersForm.html')
def exchangeorderform():
    return render_template("exchangeOrdersForm.html")

@app.route('/dogecoinTransactionsEntity.html', methods=["POST", "GET"])
def dogecointransaction():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinTransactions"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return render_template("dogecoinTransactionsEntity.html",transactions=data)

@app.route('/dogecoinTransactionsForm.html')
def dogecointransactionform():
    return render_template("dogecoinTransactionsForm.html")

@app.route('/index.html')
def reroute():
    return redirect(url_for("root"))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 36439))


    app.run(port=port, debug=True)


