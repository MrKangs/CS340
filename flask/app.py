from flask import Flask, jsonify, render_template, redirect, url_for
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
externalWalletID = {"DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy", "DAu9awAQWtbD3KR1bNKjNvtR7NhMvyGc4z", "DTJFYN36jz1qx4wLiqQ5Atj3YuxPty8HyD", "D6wm6g81qAfmZswUaB7HqkGHLWeabnDZwp", "DC74MnmyVKZfZGKFAT7Q89jLKtcWyk5EsU", "DGt8UzqzwGcMeZYS11aSrHunFJVckxFvsG", "DFvmPfgRtjAG8FFv9UuBs4ffjCkE8q9YPn", "DRWjzTVtUERKpmieESBxjwb5wH9BuBB3mA", "DDzejugjtXPUZrUtTAojBPAop4U4fYHfZn"}
dogecoinWalletAddress = {"D8XskzpskY1fGxBrfWMu65AWF1LSFeAvkF", "DEb5KeZAJKeqQ6ugoCZ6fHrBRHHkEkLdQS", "D9wfpqQU4PCZRmDpAqvH6hmau7dEBBJFTq", "DP9jzRmr54eszobQgFsvu2Qgi55DaJBmmy", "DGJNetovmNoBZiF5YymLfcc4R8LAQeewkz"}
transactionHash = {"92b1588447ab7f6857ae63185e2046a5a4aa3db0e79c8988f44a90219119245b", "7707ddd1931c7ecd937f7edd717c8c7d1cf78947d880384a5a21576ba5f155d5", "802ccc8407e45018c639b978210b1c7bba874ae701501cffb40b8af4171145f7", "38f9e947d84b45a3ad10d97dd1e2d601113858e4a982f992f35f0336ebc19e4a", "c744430e9cde0d588cfc7ce0ac5b3d58358a5351073df2d1ce3e35c7b66fc5e7", "2ff385f8f65385054668414631e4e596cc3fbbe43e57b158c56f4626b5aef359", "97576dc75a02d1381c056c403b2318346989a48f48fc7431bba4f6c300abe6bd", "ca29be2a6d1d5b57afef7daefec09a2e731faaee38e5e6a0ee2bd17aa389491f", "82b1588447ab7f6857ae63185d2046a5a4aa3db0d79c8988f44c90219119245b", "50d94ee75ee361ed84e7897a951204872fefb7c8049adc783e6877362e803e4a", "04184882ecd8db602829f04cc9453f18d822e4ef1e15032755840f007311af79", "cd8435768a7aca7537d28109889a311d1a6b647c00e0aa146887e42e1b8cb057", "1e2e6b087ac2b8f025e730d340be4dfaa7c29080a82c181c4d551919a517b506", "0bd1489941f263d0076efe3b4e980299d67ac918cba49c6b3245d5980175eeec"}

# Routes

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/entities/userAccountsEntity.html', methods=["POST", "GET"])
def user():
    if request.method == "GET":
        query = "SELECT * FROM userAccounts ORDER BY POSITION(left(userID, 1) IN 'U'), length(userID), userID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/userAccountsEntity.html", users=data, length=len(data))
    
    if request.method == "POST":
        if request.form.get("Search"):
            print("Search query")
            return render_template("/entities/userAccountsEntity.html", users=data, length=len(data))
        else:
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zipCode = request.form["zipCode"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]
            password = request.form["password"]
            global pk_userAccounts, pk_fiatWallets, pk_dogecoinWallets, dogecoinWalletAddress
            userID, pk_userAccounts = pk_generator.generate_pk_userAccounts(pk_userAccounts)
            fiatWalletID, pk_fiatWallets = pk_generator.generate_pk_fiatWallets(pk_fiatWallets)
            dogecoinWalletID, pk_dogecoinWallets = pk_generator.generate_pk_dogecoinWallets(pk_dogecoinWallets)
            walletAddress, dogecoinWalletAddress = pk_generator.generate_dogecoin_wallet_address(dogecoinWalletAddress)

            query1 = f'INSERT INTO fiatWallets (fiatWalletID, fiatBalance) VALUES ("{fiatWalletID}", {0})'
            query2 = f'INSERT INTO dogecoinWallets (dogecoinWalletID, walletAddress ,dogecoinBalance) VALUES ("{dogecoinWalletID}","{walletAddress}",{0})'
            query3 = f'INSERT INTO userAccounts (userID, firstName, lastName, address, city, state, zipCode, phoneNumber, email, password, fiatWalletID, dogecoinWalletID) VALUES ("{userID}", "{firstName}", "{lastName}", "{address}", "{city}", "{state}", "{zipCode}", "{phoneNumber}", "{email}", "{password}", "{fiatWalletID}", "{dogecoinWalletID}")'
            cur = mysql.connection.cursor()
            cur.execute(query1)
            cur.execute(query2)
            cur.execute(query3)
            mysql.connection.commit()
            return redirect(url_for("user"))

@app.route('/forms/userAccountsForm.html', methods=["GET"])
def userform():
    return render_template("/forms/userAccountsForm.html")

@app.route('/forms/userAccountsForm.html/<pk>', methods = ["POST"])
def userformupdatesearch(pk):
    # userID, dummy = pk_generator.generate_pk_userAccounts(pk)
    # query = f'SELECT * FROM userAccounts WHERE userID = "{userID}"'
    # cur = mysql.connection.cursor()
    # cur.execute(query)
    # data = cur.fetchall()
    # data = jsonify(query)
    return redirect(url_for("userform"))

@app.route('/entities/fiatWalletsEntity.html', methods=["POST", "GET"])
def fiatwallet():
    if request.method == "GET":
        query = "SELECT * FROM fiatWallets ORDER BY POSITION(left(fiatWalletID, 1) IN 'F'), length(fiatWalletID), fiatWalletID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/fiatWalletsEntity.html", fiatwallets=data, length=len(data))

    if request.method == "POST":
        if request.form.get("Search"):
            print("Search query")
            return render_template("/entities/fiatWalletsEntity.html", fiatwallets=data, length=len(data))
        else:
            fiatWalletID = request.form["fiatWalletID"]
            fiatBalance = request.form["fiatWalletBalance"]
            fiatWalletName = request.form["fiatWalletName"]
            query = f'UPDATE fiatWallets SET fiatBalance = {fiatBalance}, fiatWalletName = "{fiatWalletName} WHERE fiatWalletID = "{fiatWalletID}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("fiatwallet"))

    

@app.route('/forms/fiatWalletsForm.html')
def fiatwalletform():
    return render_template("/forms/fiatWalletsForm.html")

@app.route('/entities/dogecoinWalletsEntity.html', methods=["POST", "GET"])
def dogecoinwallet():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN 'D'), length(dogecoinWalletID), dogecoinWalletID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/dogecoinWalletsEntity.html", dogecoinWallets=data, length=len(data))
    
    if request.method == "POST":
        if request.form.get("Search"):
            print("Search query")
            return render_template("/entities/dogecoinWalletsEntity.html", dogecoinWallets=data, length=len(data))
        else:
            dogecoinWalletID = request.form["dogecoinWalletID"]
            walletAddress = request.form["walletAddress"]
            dogecoinBalance = request.form["dogecoinBalance"]
            query = f'UPDATE fiatWallets SET dogecoinBalance = {dogecoinBalance} WHERE dogecoinWalletID = "{dogecoinWalletID}" AND walletAddress = "{walletAddress}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("dogecoinwallet"))

@app.route('/forms/dogecoinWalletsForm.html')
def dogecoinwalletform():
    return render_template("/forms/dogecoinWalletsForm.html")

@app.route('/entities/exchangeOrdersEntity.html', methods=["POST", "GET"])
def exchangeorder():
    if request.method == "GET":
        query = "SELECT * FROM exchangeOrders ORDER BY POSITION(left(exchangeID, 1) IN 'E'), length(exchangeID), exchangeID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/exchangeOrdersEntity.html", exchangeOrders=data, length=len(data))
    
    if request.method == "POST":
        if request.form.get("Search"):
            print("Search query")
            return render_template("/entities/exchangeOrdersEntity.html", exchangeOrders=data, length=len(data))
        else:
            orderType = request.form["orderType"]
            orderDirection = request.form["orderDirection"]
            amountFilled = request.form["amountFilled"]
            orderPrice = request.form["orderPrice"]
            fiatWalletID = request.form["fiatWalletID"]
            dogecoinWalletID = request.form["dogecoinWalletID"]
            global pk_exchangeOrders
            exchangeID, pk_exchangeOrders = pk_generator.generate_pk_exchangeOrders(pk_exchangeOrders)
            orderTimestamp = pk_generator.get_datetime()
            query = f'INSERT INTO exchangeOrders (exchangeID, fiatWalletID, dogecoinWalletID, orderTimestamp, orderType, orderDirection, amountFilled, orderPrice) VALUES ("{exchangeID}", "{fiatWalletID}", "{dogecoinWalletID}", "{orderTimestamp}","{orderType}", "{orderDirection}", {amountFilled}, {orderPrice})'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("exchangeorder"))
    

@app.route('/forms/exchangeOrdersForm.html')
def exchangeorderform():
    return render_template("/forms/exchangeOrdersForm.html")

@app.route('/entities/dogecoinTransactionsEntity.html', methods=["POST", "GET"])
def dogecointransaction():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinTransactions ORDER BY POSITION(left(txID, 1) IN 'T'), length(txID), txID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/dogecoinTransactionsEntity.html",transactions=data, length=len(data))
    
    if request.method == "POST":
        if request.form.get("Search"):
            print("Search query")
            return render_template("/entities/dogecoinTransactionsEntity.html", transactions=data, length=len(data))
        else:
            amount = request.form["amount"]
            txDirection = request.form["txDirection"]
            dogecoinWalletID = request.form["dogecoinWalletID"]
            global externalWalletID, pk_dogecoinTransactions, transactionHash
            txID, pk_dogecoinTransactions = pk_generator.generate_pk_dogecoinTransactions(pk_dogecoinTransactions)
            externalWalletAddress, externalWalletID = pk_generator.generate_external_wallet_id(externalWalletID)
            txHash, transactionHash = pk_generator.generate_transaction_hash(transactionHash)
            txTimestamp = pk_generator.get_datetime()
            query = f'INSERT INTO dogecoinTransactions (txID, txTimestamp, amount, txDirection, dogecoinWalletID, externalWalletAddress, txHash) VALUES ("{txID}", "{txTimestamp}", {amount},"{txDirection}", "{dogecoinWalletID}", "{externalWalletAddress}", "{txHash}")'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("dogecointransaction"))

@app.route('/forms/dogecoinTransactionsForm.html')
def dogecointransactionform():
    return render_template("/forms/dogecoinTransactionsForm.html")

@app.route('/index.html')
def reroute():
    return redirect(url_for("root"))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 36439))


    app.run(port=port, debug=True)


