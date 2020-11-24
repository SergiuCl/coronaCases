from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from apscheduler.schedulers.background import BackgroundScheduler
from coronaCasesDAO import select_cases, get_cases_world, select_cases_where_country, select_countries, select_history_for_country, select_distinct_data, select_maximum_cases, select_specific_cases
from subscribeDAO import select_user, insert_user, remove_user, select_all_users, update_user, update_name_country, delete_where_userID, select_user_where_email, isert_user_into_users
from helpers import get_news, get_dict_news, dict_factory, get_value_list, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import requests
import json
import time, threading


# Configure application
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def Index():
    
    # get API News
    mylist = get_news()
    return render_template('index.html', context = mylist)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get email Address from user
        email = request.form.get("email")

        # query database for email    
        rows = select_user_where_email('users', email)

        # Ensure email exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('invalid username and/or password', 'error')
            return redirect(url_for('login'))

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to users panel
        return redirect(url_for('usersTable'))
        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        emailAddress = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        passwordConfirm = request.form.get("confirmation")

        # check if username exists in db
        checkUser = select_user('users', emailAddress)
        if bool(checkUser):
            flash('Email Address already exists', 'info')
            return redirect(url_for('register'))
        else:
            if passwordConfirm != password:
                flash('Please confirm your password', 'error')
                return(url_for('register'))
            
            # hash password
            hashPsw = generate_password_hash(password)
            role = 'user'
            isert_user_into_users('users', emailAddress, name, hashPsw, role)
            flash('You have been succesfully registered')
            return redirect(url_for('usersTable'))
    else:
        return render_template("register.html")


@app.route("/news/<content>")
def show_item_info(content):
    
    # get news in dictionary
    mylist = get_dict_news()
    contentImg = None
    title = None
    # for every row in dict
    # ensure content corresponds to title
    for row in mylist:
        if content in row['title']:
            content = row['content']
            contentImg = row['urlToImage']
            title = row['title']

    return render_template('news.html', content=content, i=contentImg, title=title)


@app.route("/casesInAustria")
def casesInAustria():
    
    # get the cases for Austria and show them in the table
    tblCasesWorld = "casesWorld"
    country = "Austria"
    tableValues = {}
    tableValues = select_cases_where_country(tblCasesWorld, country)
    return render_template('casesInAustria.html', casesAustria=tableValues)


@app.route("/casesWorld")
def casesWorld():

    # get all the cases and show them in table
    tblCasesWorld = "casesWorld"
    tableValues = {}
    totalCases = {}
    tableValues = select_cases(tblCasesWorld)
    totalCases = select_cases_where_country(tblCasesWorld, "World")
    return render_template('casesWorld.html', casesWorld=tableValues, totalCases=totalCases)


@app.route("/history/<content>")
def cases_history(content):

    tblHistory = "history"
    tableValues = select_cases("casesWorld")
    if bool(tableValues):
        for row in tableValues:
            if content in row['country']:
                content = row['country']
                # get the dates for the chart
                historyDates = select_distinct_data(tblHistory)
                dates = []
                # append the dates to the list dates
                dates = get_value_list(historyDates, "date")

                newCasesHistory = select_specific_cases("history", "new", content)
                activeCasesHistory = select_specific_cases("history", "active", content)
                deathsHistory = select_specific_cases("history", "deaths", content)

                newCasesHistoryList = []
                newCasesHistoryList = get_value_list(newCasesHistory, "new")
                activeCasesHistoryList = []
                activeCasesHistoryList = get_value_list(activeCasesHistory, "active")
                deathsHistoryList = []
                deathsHistoryList = get_value_list(deathsHistory, "deaths")

    return render_template('history.html', content=content, newCases=json.dumps(newCasesHistoryList), active=json.dumps(activeCasesHistoryList), newDeaths=json.dumps(deathsHistoryList), dates=json.dumps(dates))


@app.route("/subscription", methods=["GET", "POST"])
def subscribe():

    if request.method == "POST":
         
         # get the data from user
        emailAdress = request.form.get("email")
        name = request.form.get("name")
        unsubscribe = request.form.get("unsubscribe")
        country = request.form.get("countries")

        # ensure user provide an email and a name
        if not emailAdress:
            flash("Please provide an email")
        elif not name:
            flash("Please provide a name")
        elif not country:
            flash("Please choose a country")
        else:
            # if user checked the box unsubscribe
            # remove user from table
            if unsubscribe:
                # check if user exists
                # if exists, inform him
                checkUser = select_user('subscribers', emailAdress)
                if bool(checkUser):
                    remove_user(emailAdress)
                    flash('You have successfully unsubscribed', 'success')
                    return redirect(url_for('subscribe'))
                else:
                    flash('You are not a subscriber of our newsletter', 'info')
                    return redirect(url_for('subscribe'))
            else:
                # check if user already exists
                checkUser = select_user('subscribers', emailAdress)

                # check if query returns any values
                # if yes, inform the user that he already subscribed
                # else, insert the user info in the database
                if bool(checkUser):
                    flash('You have already subscribed to our newsletter', 'info')
                    return redirect(url_for('subscribe'))
                else:
                    insert_user(emailAdress, name, country)
                    flash('You have successfully subscribed', 'success')
                    return redirect(url_for('subscribe'))
    else:
        countries = select_countries("casesWorld")
        countriesList = []
        countriesList = get_value_list(countries, "country")

        return render_template("subscription.html", countries=countriesList)


@app.route("/usersTable")
@login_required
def usersTable():

    # get data for table
    users = select_all_users()
    return render_template("usersTable.html", users=users)


@app.route("/usersTable/delete/<emailAddress>/<int:userID>")
def deleteUser(emailAddress, userID):

    # delete user from table based on url
    delete_where_userID(userID)
    return redirect(url_for('usersTable'))


@app.route("/manageUsers/<action>/<emailAddress>/<int:userID>", methods=["GET", "POST"])
def manageUsers(action, emailAddress, userID):
    
    if request.method == "POST":

        if action == "create":
            # get the data from user
            email = request.form.get("email")
            name = request.form.get("name")
            country = request.form.get("countries")
            # ensure user provide an email and a name
            if not email:
                flash("Please provide an email")
            elif not name:
                flash("Please provide a name")
            elif not country:
                flash("Please choose a country")
            else:
                # check if user already exists
                checkUser = select_user('subscribers', email)
                """ check if query returns any values
                if yes, inform the user
                else insert it into th table """
                if bool(checkUser):
                    flash('The specified user already exists', "info")
                    return redirect(url_for('manageUsers', action=action, emailAddress=emailAddress, userID=userID))
                else:
                    insert_user(email, name, country)
                    flash('The user has been successfully created', 'success')
                    return redirect(url_for('manageUsers', action=action, emailAddress=emailAddress, userID=userID))
        elif action == "edit":
            # get the data from user
            name = request.form.get("name")
            country = request.form.get("countries")

            if not name:
                update_user(userID, country)
                flash('The user has been successfully updated', 'success')
                return redirect(url_for('manageUsers', action=action, emailAddress=emailAddress, userID=userID))
            else:
                update_name_country(userID, country, name)
                flash('The user has been successfully updated', 'success')
                return redirect(url_for('manageUsers', action=action, emailAddress=emailAddress, userID=userID))
    else:
        query = action
        countries = select_countries("casesWorld")
        countriesList = []
        countriesList = get_value_list(countries, "country")
        action = request.form.get("querys")

        return render_template("manageUsers.html", query=query, countries=countriesList, emailAddress=emailAddress)


# set a background scheduler
scheduler = BackgroundScheduler()
# set a scheduler with interval 10 minutes  
job1 = scheduler.add_job(get_cases_world, 'interval', minutes=10)
# start the scheduler
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
