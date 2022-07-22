# Sample Flask application for a BSG database, snapshot of BSG_people

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_OSUusername"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_OSUusername"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/people")


# route for people page
@app.route("/people", methods=["POST", "GET"])
def people():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Person"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if age == "" and homeworld == "0":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO bsg_people (fname, lname) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "INSERT INTO bsg_people (fname, lname, age) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age))
                mysql.connection.commit()

            # account for null age
            elif age == "":
                query = "INSERT INTO bsg_people (fname, lname, homeworld) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO bsg_people (fname, lname, homeworld, age) VALUES (%s, %s,%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/people")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT bsg_people.id, fname, lname, bsg_planets.name AS homeworld, age FROM bsg_people LEFT JOIN bsg_planets ON homeworld = bsg_planets.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("people.j2", data=data, homeworlds=homeworld_data)


# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_people/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM bsg_people WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/people")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_people/<int:id>", methods=["POST", "GET"])
def edit_people(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form["personID"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=3000, debug=True)
