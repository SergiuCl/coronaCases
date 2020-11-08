from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from cs50 import SQL
from apscheduler.schedulers.background import BackgroundScheduler
from dbQRYsCoronaCases import select_cases, get_cases_world, select_cases_where_country
from dbQRYsSubscribe import select_user, insert_user, remove_user, select_all_users
from helpers import get_news, get_dict_news
import requests
import json
import time, threading


# Configure application
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = SQL("sqlite:///coronaDatabase.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def Index():
    
    # get API News
    mylist = get_news()
    return render_template('index.html', context = mylist)



@app.route("/news/<content>")
def show_item_info(content):
    
    # get news in dictionary
    mylist = get_dict_news()

    # for every row in dict
    # ensure content corresponds to title
    for row in mylist:
        if content in row['title']:
            content = row['content']
            contentImg = row['urlToImage']

# https://pythonise.com/series/learning-flask/generating-dynamic-urls-with-flask        
    return render_template('news.html', content=content, i=contentImg)




@app.route("/casesInAustria")
def casesInAustria():
    
    tblCasesWorld = "casesWorld"
    country = "Austria"
    tableValues = {}
    tableValues = select_cases_where_country(tblCasesWorld, country)
    return render_template('casesInAustria.html', casesAustria=tableValues)



@app.route("/casesWorld")
def casesWorld():

    tblCasesWorld = "casesWorld"
    tableValues = {}
    totalCases = {}
    tableValues = select_cases(tblCasesWorld)
    totalCases = select_cases_where_country(tblCasesWorld, "World")
    return render_template('casesWorld.html', casesWorld=tableValues, totalCases=totalCases)


@app.route("/history/<content>")
def cases_history(content):

    tableValues = select_cases("casesWorld")
    if bool(tableValues):
        for row in tableValues:
            if content in row['country']:
                content = row['country']

    return render_template('history.html', context=content)


@app.route("/subscription", methods=["GET", "POST"])
def subscribe():
    if request.method == "POST":
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
            print(country)
            # if user checked the box unsubscribe
            # remove user from table
            if unsubscribe:
                # check if user exists
                # if exists, inform him
                checkUser = select_user(emailAdress)
                if bool(checkUser):
                    remove_user(emailAdress)
                    flash('You have successfully unsubscribed')
                    return redirect(url_for('subscribe'))
                else:
                    flash('You are not a subscriber of our newsletter', 'success')
                    return redirect(url_for('subscribe'))
            else:
                # check if user already exist
                checkUser = select_user(emailAdress)

                # check if query returns any values
                # if yes, inform the user that he already subscribed
                # else, insert the user info in the database
                if bool(checkUser):
                    flash('You have already subscribed to our newsletter')
                    return redirect(url_for('subscribe'))
                else:
                    insert_user(emailAdress, name, country)
                    flash('You have successfully subscribed', 'success')
                    return redirect(url_for('subscribe'))
    else:
        countries = db.execute("SELECT country FROM casesWorld")
        countriesList = []

        for i in range(len(countries)):
            countriesList.append(countries[i]['country'])

        return render_template("subscription.html", countries=countriesList)




# set a background scheduler
scheduler = BackgroundScheduler()
# set a scheduler with interval 3 minute    
job1 = scheduler.add_job(get_cases_world, 'interval', minutes=0.2)
# start the scheduler
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)