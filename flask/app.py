from operator import imod
import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask import request
import time
import static.py.autogenerator as pk_generator
import static.py.validator as validator
import static.py.string_parser as sp
import static.py.webdriver as wd

# Configuration

app = Flask(__name__)
app.secret_key = os.urandom(12)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_kangken'
app.config['MYSQL_PASSWORD'] = '8280' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_kangken'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Variables

pk_userAccounts = 5
pk_fiatWallets = 5
pk_dogecoinWallets = 5
pk_exchangeOrders = 18
pk_dogecoinTransactions = 14
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
        request_values = request.form
        if bool(request_values.get("search")):
            return redirect(url_for("searchForUserAccount", data=request.form["search"]))

        elif bool(request_values.get("userID")):
            if validator.validate_user_input(request.form["email"]) == False:
                flash("There is an issue with the email input. Please update the email field correctly!")
                return redirect(url_for("user"))
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zipCode = request.form["zipCode"]
            phoneNumber = request.form["phoneNumber"]
            email = request.form["email"]
            password = request.form["password"]
            userID = request.form["userID"]
            query = f'UPDATE userAccounts SET firstName = "{firstName}", lastName = "{lastName}", address = "{address}", city = "{city}", state = "{state}", zipCode = "{zipCode}", phoneNumber = "{phoneNumber}", email = "{email}", password = "{password}" WHERE userID = "{userID}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("user"))
        else:
            if validator.validate_user_input(request.form["email"]) == False:
                flash("There is an issue with the email input. Please update the email field correctly!")
                return redirect(url_for("user"))
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

@app.get('/entities/userAccountsEntity.html?data=<data>')
def searchForUserAccount(data):
    firstName, lastName = data.split()
    query = f'SELECT * FROM userAccounts WHERE firstName = "{firstName}" AND lastName = "{lastName}" ORDER BY POSITION(left(userID, 1) IN "U"), length(userID), userID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/entities/userAccountsEntity.html", users=data, length=len(data))

@app.route('/forms/userAccountsForm.html')
def renderUserAccountsForm():
    return render_template("/forms/userAccountsForm.html", user="nothing")

@app.route('/forms/userAccountsForm.html/<inputdata>', methods=["POST", "GET"])
def updateUserAccount(inputdata):
    if request.method == "POST":
        return redirect(url_for("updateUserAccount", inputdata=inputdata))
    if request.method == "GET":
        query = f'SELECT * FROM userAccounts WHERE userID = "{inputdata}"'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchone()
        return render_template("/forms/userAccountsForm.html", user=data)

# Delete user account.
@app.route('/entities/userAccountsEntity.html/<inputdata>/delete', methods=["POST", "GET"])
def deleteUserAccount(inputdata):

    if request.method == "POST":        
        fiatWalletPKString = sp.replace_char(inputdata, "U", "F")
        selectedFiatWalletPKs = sp.splitPKString(fiatWalletPKString)
        dogecoinWalletPKString = sp.replace_char(inputdata, "U", "D")
        selectedDogecoinWalletPKs = sp.splitPKString(dogecoinWalletPKString)
        selectedUserPKs = sp.splitPKString(inputdata)

        for pkIndex in range(len(selectedUserPKs)):
            userAccountQuery = f'DELETE FROM userAccounts WHERE userID = "{selectedUserPKs[pkIndex]}"'
            fiatWalletQuery = f'DELETE FROM fiatWallets WHERE fiatWalletID = "{selectedFiatWalletPKs[pkIndex]}"'
            dogecoinWalletQuery = f'DELETE FROM dogecoinWallets WHERE dogecoinWalletID = "{selectedDogecoinWalletPKs[pkIndex]}"'

            cur = mysql.connection.cursor()
            cur.execute(userAccountQuery)
            cur.execute(fiatWalletQuery)
            cur.execute(dogecoinWalletQuery)
            mysql.connection.commit()

        return redirect(url_for("user"))




@app.route('/entities/fiatWalletsEntity.html', methods=["POST", "GET"])
def fiatwallet():
    if request.method == "GET":
        query = "SELECT * FROM fiatWallets ORDER BY POSITION(left(fiatWalletID, 1) IN 'F'), length(fiatWalletID), fiatWalletID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/fiatWalletsEntity.html", fiatwallets=data, length=len(data))

    if request.method == "POST":
        request_values = request.form
        if bool(request_values.get("search")):
            return redirect(url_for("searchFiatWallet", data=request.form["search"]))
        else:
            if validator.validate_fiatwallet_input(request.form["fiatWalletBalance"]) == False:
                flash("There is an issue with the balance input. Please update the Fiat Wallet Balance correctly!")
                return redirect(url_for("fiatwallet"))
            fiatWalletID = request.form["fiatWalletID"]
            fiatBalance = request.form["fiatWalletBalance"]
            fiatWalletName = request.form["fiatWalletName"]
            query = f'UPDATE fiatWallets SET fiatBalance = {fiatBalance}, fiatWalletName = "{fiatWalletName}" WHERE fiatWalletID = "{fiatWalletID}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("fiatwallet"))

@app.get('/entities/fiatWalletsEntity.html?data=<data>')
def searchFiatWallet(data):
    firstName, lastName = data.split()
    query = f'SELECT fiatWallets.fiatWalletID, fiatWallets.fiatWalletName,fiatWallets.fiatBalance FROM fiatWallets INNER JOIN userAccounts ON fiatWallets.fiatWalletID = userAccounts.fiatWalletID WHERE userAccounts.firstName = "{firstName}" AND userAccounts.lastName = "{lastName}" ORDER BY POSITION(left(fiatWallets.fiatWalletID, 1) IN "F"), length(fiatWallets.fiatWalletID), fiatWallets.fiatWalletID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/entities/fiatWalletsEntity.html", fiatwallets=data, length=len(data))

@app.route('/forms/fiatWalletsForm.html/<inputdata>', methods=["POST", "GET"])
def updateFiatWallet(inputdata):
    if request.method == "POST":
        return redirect(url_for("updateFiatWallet",inputdata=inputdata))
    if request.method == "GET":
        query = f'SELECT * FROM fiatWallets WHERE fiatWalletID = "{inputdata}"'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchone()
        return render_template("/forms/fiatWalletsForm.html", fiatwallet=data)

# Delete fiat wallet.
@app.route('/entities/fiatWalletsEntity.html/<inputdata>/delete', methods=["POST"])
def deleteFiatWallet(inputdata):
    if request.method == "POST":
        userAccountPKString = sp.replace_char(inputdata, "F", "U")
        selectedUserAccountPKs = sp.splitPKString(userAccountPKString)
        dogecoinWalletPKString = sp.replace_char(inputdata, "F", "D")
        selectedDogecoinWalletPKs = sp.splitPKString(dogecoinWalletPKString)
        selectedFiatWalletPKs = sp.splitPKString(inputdata)

        for pkIndex in range(len(selectedFiatWalletPKs)):
            fiatWalletQuery = f'DELETE FROM fiatWallets WHERE fiatWalletID = "{selectedFiatWalletPKs[pkIndex]}"'
            userAccountQuery = f'DELETE FROM userAccounts WHERE userID = "{selectedUserAccountPKs[pkIndex]}"'
            dogecoinWalletQuery = f'DELETE FROM dogecoinWallets WHERE dogecoinWalletID = "{selectedDogecoinWalletPKs[pkIndex]}"'
            cur = mysql.connection.cursor()
            cur.execute(userAccountQuery)
            cur.execute(fiatWalletQuery)
            cur.execute(dogecoinWalletQuery)
            mysql.connection.commit()

    return redirect(url_for("fiatwallet"))


@app.route('/entities/dogecoinWalletsEntity.html', methods=["POST", "GET"])
def dogecoinwallet():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN 'D'), length(dogecoinWalletID), dogecoinWalletID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/dogecoinWalletsEntity.html", dogecoinWallets=data, length=len(data))

    if request.method == "POST":
        request_values = request.form
        if bool(request_values.get("search")):
            return redirect(url_for("searchForDogecoinWallet", data=request.form["search"]))
        else:
            if validator.validate_dogecoinwallet_input(request.form["dogecoinBalance"]) == False:
                flash("There is an issue with the balance input. Please update the Dogecoin Wallet Balance correctly!")
                return redirect(url_for("dogecoinwallet"))
            dogecoinWalletID = request.form["dogecoinWalletID"]
            walletAddress = request.form["walletAddress"]
            dogecoinBalance = request.form["dogecoinBalance"]
            query = f'UPDATE dogecoinWallets SET dogecoinBalance = {dogecoinBalance} WHERE dogecoinWalletID = "{dogecoinWalletID}" AND walletAddress = "{walletAddress}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("dogecoinwallet"))

@app.get('/entities/dogecoinWalletsEntity.html?data=<data>')
def searchForDogecoinWallet(data):
    firstName, lastName = data.split()
    query = f'SELECT dogecoinWallets.dogecoinWalletID, dogecoinWallets.walletAddress, dogecoinWallets.dogecoinBalance FROM dogecoinWallets INNER JOIN userAccounts ON dogecoinWallets.dogecoinWalletID = userAccounts.dogecoinWalletID WHERE userAccounts.firstName = "{firstName}" AND userAccounts.lastName = "{lastName}" ORDER BY POSITION(left(dogecoinWallets.dogecoinWalletID, 1) IN "D"), length(dogecoinWallets.dogecoinWalletID), dogecoinWallets.dogecoinWalletID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/entities/dogecoinWalletsEntity.html", dogecoinWallets=data, length=len(data))

@app.route('/forms/dogecoinWalletsForm.html')
def dogecoinwalletform():
    return render_template("/forms/dogecoinWalletsForm.html")

@app.route('/forms/dogecoinWalletsForm.html/<inputdata>', methods=["POST", "GET"])
def updateDogecoinWallet(inputdata):
    if request.method == "POST":
        return redirect(url_for("updateDogecoinWallet",inputdata=inputdata))
    if request.method == "GET":
        query = f'SELECT * FROM dogecoinWallets WHERE dogecoinWalletID = "{inputdata}"'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchone()
        return render_template("/forms/dogecoinWalletsForm.html", dogecoinwallet=data)

# Delete dogecoin wallet.
@app.route('/entities/dogecoinWalletsEntity.html/<inputdata>/delete', methods=["POST"])
def deleteDogecoinWallet(inputdata):
    if request.method == "POST":
        userAccountPKString = sp.replace_char(inputdata, "D", "U")
        selectedUserAccountPKs = sp.splitPKString(userAccountPKString)
        fiatWalletPKString = sp.replace_char(inputdata, "D", "F")
        selectedFiatWalletPKs = sp.splitPKString(fiatWalletPKString)
        selectedDogecoinWalletPKs = sp.splitPKString(inputdata)

        for pkIndex in range(len(selectedDogecoinWalletPKs)):
            dogecoinWalletQuery = f'DELETE FROM dogecoinWallets WHERE dogecoinWalletID = "{selectedDogecoinWalletPKs[pkIndex]}"'
            userAccountQuery = f'DELETE FROM userAccounts WHERE userID = "{selectedUserAccountPKs[pkIndex]}"'
            fiatWalletQuery = f'DELETE FROM fiatWallets WHERE fiatWalletID = "{selectedFiatWalletPKs[pkIndex]}"'
            cur = mysql.connection.cursor()
            cur.execute(dogecoinWalletQuery)
            cur.execute(userAccountQuery)
            cur.execute(fiatWalletQuery)
            mysql.connection.commit()

    return redirect(url_for("fiatwallet"))

@app.route('/entities/exchangeOrdersEntity.html', methods=["POST", "GET"])
def exchangeorder():
    if request.method == "GET":
        query = "SELECT * FROM exchangeOrders ORDER BY POSITION(left(exchangeID, 1) IN 'E'), length(exchangeID), exchangeID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/exchangeOrdersEntity.html", exchangeOrders=data, length=len(data))

    if request.method == "POST":
        request_values = request.form
        if bool(request_values.get("search")):
            return redirect(url_for("searchForExchangeOrder", data=request.form["search"]))

        elif bool(request_values.get("exchangeID")):
            if validator.validate_exchangeorder_input(request.form["amountFilled"], request.form["orderPrice"], request.form["fiatWalletID"], request.form["dogecoinWalletID"]) == False:
                flash("There is an issue with the Order Price input, Amount Filled input, Dogecoin Wallet ID input, or Fiat Wallet ID input. Please update the form correctly!")
                return redirect(url_for("exchangeorder"))
            orderType = request.form["orderType"]
            orderDirection = request.form["orderDirection"]
            amountFilled = request.form["amountFilled"]
            orderPrice = request.form["orderPrice"]
            fiatWalletID = request.form["fiatWalletID"]
            dogecoinWalletID = request.form["dogecoinWalletID"]
            exchangeID = request.form["exchangeID"]
            orderTimestamp = pk_generator.get_datetime()
            query = f'UPDATE exchangeOrders SET orderType = "{orderType}", orderDirection= "{orderDirection}", amountFilled = {amountFilled}, orderPrice = {orderPrice}, fiatWalletID = "{fiatWalletID}", dogecoinWalletID = "{dogecoinWalletID}", orderTimestamp = "{orderTimestamp}" WHERE exchangeID = "{exchangeID}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("exchangeorder"))
        else:
            if validator.validate_exchangeorder_input(request.form["amountFilled"], request.form["orderPrice"], request.form["fiatWalletID"], request.form["dogecoinWalletID"]) == False:
                flash("There is an issue with the Order Price input, Amount Filled input, Dogecoin Wallet ID input, or Fiat Wallet ID input. Please update the form correctly!")
                return redirect(url_for("exchangeorder"))
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

@app.get('/entities/exchangeOrdersEntity.html?data=<data>')
def searchForExchangeOrder(data):
    firstName, lastName = data.split()
    query = f'SELECT exchangeOrders.exchangeID, exchangeOrders.fiatWalletID, exchangeOrders.dogecoinWalletID, exchangeOrders.orderTimestamp, exchangeOrders.orderType, exchangeOrders.orderDirection, exchangeOrders.amountFilled, exchangeOrders.orderPrice FROM exchangeOrders INNER JOIN dogecoinWallets ON dogecoinWallets.dogecoinWalletID = exchangeOrders.dogecoinWalletID INNER JOIN userAccounts ON userAccounts.dogecoinWalletID = dogecoinWallets.dogecoinWalletID WHERE userAccounts.firstName = "{firstName}" AND userAccounts.lastName = "{lastName}" ORDER BY POSITION(left(exchangeOrders.exchangeID, 1) IN "E"), length(exchangeOrders.exchangeID), exchangeOrders.exchangeID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/entities/exchangeOrdersEntity.html", exchangeOrders=data, length=len(data))


@app.route('/forms/exchangeOrdersForm.html')
def exchangeorderform():
    query = f'SELECT dogecoinWalletID FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN "D"), length(dogecoinWalletID), dogecoinWalletID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    pk1 = cur.fetchall()
    query = f'SELECT fiatWalletID FROM fiatWallets ORDER BY POSITION(left(fiatWalletID, 1) IN "F"), length(fiatWalletID), fiatWalletID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    pk2 = cur.fetchall()
    return render_template("/forms/exchangeOrdersForm.html", order="nothing", pk1=pk1, pk2=pk2)

@app.route('/forms/exchangeOrdersForm.html/<inputdata>', methods=["POST", "GET"])
def updateExchangeOrder(inputdata):
    if request.method == "POST":
        return redirect(url_for("updateExchangeOrder",inputdata=inputdata))
    if request.method == "GET":
        query = f'SELECT * FROM exchangeOrders WHERE exchangeID = "{inputdata}"'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchone()
        query = f'SELECT dogecoinWalletID FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN "D"), length(dogecoinWalletID), dogecoinWalletID'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pk1 = cur.fetchall()
        query = f'SELECT fiatWalletID FROM fiatWallets ORDER BY POSITION(left(fiatWalletID, 1) IN "F"), length(fiatWalletID), fiatWalletID'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pk2 = cur.fetchall()
        return render_template("/forms/exchangeOrdersForm.html", order=data, pk1=pk1, pk2=pk2)
    
# Delete exchange order.
@app.route('/entities/exchangeOrdersEntity.html/<inputdata>/delete', methods=["POST"])
def deleteExchangeOrder(inputdata):
    if request.method == "POST":
        selectedExchangeOrderPKs = sp.splitPKString(inputdata)

        for primaryKey in selectedExchangeOrderPKs:
            query = f'DELETE FROM exchangeOrders WHERE exchangeID = "{primaryKey}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()

    return redirect(url_for("exchangeorder"))

@app.route('/entities/dogecoinTransactionsEntity.html', methods=["POST", "GET"])
def dogecointransaction():
    if request.method == "GET":
        query = "SELECT * FROM dogecoinTransactions ORDER BY POSITION(left(txID, 1) IN 'T'), length(txID), txID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/entities/dogecoinTransactionsEntity.html",transactions=data, length=len(data))

    if request.method == "POST":
        request_values = request.form
        if bool(request_values.get("search")):
            return redirect(url_for("searchForDogecoinTransaction", data=request.form["search"]))

        elif bool(request_values.get("txID")):
            if validator.validate_dogecointransaction_input(request.form["amount"], request.form["dogecoinWalletID"]) == False:
                flash("There is an issue with the Dogecoin Amount input or Dogecoin Wallet ID input. Please update the form correctly!")
                return redirect(url_for("dogecointransaction"))
            amount = request.form["amount"]
            txDirection = request.form["txDirection"]
            dogecoinWalletID = request.form["dogecoinWalletID"]
            txID = request.form["txID"]
            externalWalletAddress = request.form["externalWalletAddress"]
            txHash = request.form["txHash"]
            txTimestamp = pk_generator.get_datetime()
            query = f'UPDATE dogecoinTransactions SET amount = {amount}, txDirection = "{txDirection}", dogecoinWalletID = "{dogecoinWalletID}", externalWalletAddress= "{externalWalletAddress}", txHash = "{txHash}", txTimestamp = "{txTimestamp}" WHERE txID = "{txID}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()
            return redirect(url_for("dogecointransaction"))

        else:
            if validator.validate_dogecointransaction_input(request.form["amount"], request.form["dogecoinWalletID"]) == False:
                flash("There is an issue with the Dogecoin Amount input or Dogecoin Wallet ID input. Please update the form correctly!")
                return redirect(url_for("dogecointransaction"))
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


@app.get('/entities/dogecoinTransactionsEntity.html?data=<data>')
def searchForDogecoinTransaction(data):
    firstName, lastName = data.split()
    query = f'SELECT dogecoinTransactions.txID, dogecoinTransactions.txTimestamp, dogecoinTransactions.amount, dogecoinTransactions.txDirection, dogecoinTransactions.dogecoinWalletID, dogecoinTransactions.externalWalletAddress, dogecoinTransactions.txHash FROM dogecoinTransactions INNER JOIN dogecoinWallets ON dogecoinWallets.dogecoinWalletID = dogecoinTransactions.dogecoinWalletID INNER JOIN userAccounts ON userAccounts.dogecoinWalletID = dogecoinWallets.dogecoinWalletID WHERE userAccounts.firstName  ="{firstName}" AND userAccounts.lastName = "{lastName}" ORDER BY POSITION(left(dogecoinTransactions.txID, 1) IN "T"), length(dogecoinTransactions.txID), dogecoinTransactions.txID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/entities/dogecoinTransactionsEntity.html", transactions=data, length=len(data))


@app.route('/forms/dogecoinTransactionsForm.html')
def dogecointransactionform():
    query = f'SELECT dogecoinWalletID FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN "D"), length(dogecoinWalletID), dogecoinWalletID'
    cur = mysql.connection.cursor()
    cur.execute(query)
    pk = cur.fetchall()
    return render_template("/forms/dogecoinTransactionsForm.html", dogecointransaction="nothing", dogecoinwalletID=pk)

@app.route('/forms/dogecoinTransactionsForm.html/<inputdata>', methods=["POST", "GET"])
def updateDogecoinTransaction(inputdata):
    if request.method == "POST":
        return redirect(url_for("updateDogecoinTransaction",inputdata=inputdata))
    if request.method == "GET":
        query = f'SELECT * FROM dogecoinTransactions WHERE txID = "{inputdata}"'
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchone()
        query = f'SELECT dogecoinWalletID FROM dogecoinWallets ORDER BY POSITION(left(dogecoinWalletID, 1) IN "D"), length(dogecoinWalletID), dogecoinWalletID'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pk = cur.fetchall()
        return render_template("/forms/dogecoinTransactionsForm.html", dogecointransaction=data, dogecoinwalletID=pk)

# Delete dogecoin transaction.
@app.route('/entities/dogecoinTransactionsEntity.html/<inputdata>/delete', methods=["POST"])
def deleteDogecoinTransaction(inputdata):
    if request.method == "POST":
        selectedDogecoinTransactionPKs = sp.splitPKString(inputdata)

        for primaryKey in selectedDogecoinTransactionPKs:
            query = f'DELETE FROM dogecoinTransactions WHERE txID = "{primaryKey}"'
            cur = mysql.connection.cursor()
            cur.execute(query)
            mysql.connection.commit()

    return redirect(url_for("dogecointransaction"))

@app.route('/index.html')
def reroute():
    return redirect(url_for("root"))

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 36438))


    app.run(port=port, debug=True)


