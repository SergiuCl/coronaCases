from cs50 import SQL
from helpers import get_API_News_austria, get_API_News_world, convert_to_int
from datetime import date, datetime
from send import email_to_subscribers
import http.client
import json


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///coronaDatabase.db")

# define global variables
notAvailable = "N/A"
keyLastUpdate = "Last Update"



def get_cases_world():

    # load the data in JSON
    casesWorld = get_API_News_world()
    # call the function to update the table
    update_cases_world(casesWorld)
       
    


def update_cases_world(APIData):
    tblCasesWorld = "casesWorld"
    # get the values from table, WHERE country is "world" - that means the total number of cases
    country = "World"
    tblValues = select_cases_where_country(tblCasesWorld, country)
    # ensure dict is not None
    # if the value did not change, exit function
    # else, update the table
    if bool(tblValues):
        # compare the values from table with the values from API
        if tblValues[0]['totalCases'] == APIData[0]['Total Cases_text']:
            return
        else:
            update_query_world(APIData)
            # if new data, insert it into history
            #insert_into_history(APIData)
            # send an email to subscribers
            email_to_subscribers()
    else:
        insert_query(APIData)
        #insert_into_history(APIData)



def insert_query(APIData):

    # for each row in APIData
    for row in APIData:
        db.execute("""INSERT INTO casesWorld
                        (country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date)
                        VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :date)""",
                    
            countryName=row['Country_text'],
            activeCases=convert_to_int(row['Active Cases_text']),
            newCases=convert_to_int(row['New Cases_text']),
            newDeaths=convert_to_int(row['New Deaths_text']),
            totalCases=convert_to_int(row['Total Cases_text']),
            totalDeaths=convert_to_int(row['Total Deaths_text']),
            totalRecovered=convert_to_int(row['Total Recovered_text']),
            date=select_unixepoch_date())
            
    #db.commit()
    # send an email to subscribers
    #email_to_subscribers(APIData[0]['Total Cases_text'], APIData[0]['New Cases_text'])
    email_to_subscribers()



def insert_into_history(APIData):

    today = date.today()
    tblHistory = "historyWorld"
    todayValues = {}
    # for each row in APIData
    for row in APIData:
        # many key errors in code - try to handle the errors with a try block
        #try:
        todayValues = select_cases_where_country_date(tblHistory, row['Country_text'], today)
        #except KeyError:
        #    continue
        """
        check if today date for current country is already in the database
         if so, check if it needs to be updated
        """ 
        if bool(todayValues):
            continue
            #if todayValues[0]['totalCases'] != row['Total Cases_text']:
            #    update_tblHistory(tblHistory, row, today)
            #else:
            #    continue
            
        else:
            db.execute("""INSERT INTO historyWorld
                            (country, activeCases, newCases, newDeaths, totalCases, totalDeaths, totalRecovered, date)
                            VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :date)""",

                countryName=row['Country_text'],
                activeCases=row['Active Cases_text'],
                newCases=row['New Cases_text'],
                newDeaths=row['New Deaths_text'],
                totalCases=row['Total Cases_text'],
                totalDeaths=row['Total Deaths_text'],
                totalRecovered=row['Total Recovered_text'],
                date=today)
    db.commit()



def update_query_world(APIData):

    for row in APIData:
        db.execute("""UPDATE casesWorld
                        SET active = :activeCases,
                        new = :newCases,
                        deaths = :newDeaths,
                        totalCases = :totalCases,
                        totalDeaths = :totalDeaths,
                        totalRecovered = :totalRecovered,
                        WHERE country= :countryName""",
                
            activeCases=convert_to_int(row['Active Cases_text']),
            newCases=convert_to_int(row['New Cases_text'][1:]),
            newDeaths=convert_to_int(row['New Deaths_text'][1:]),
            totalCases=convert_to_int(row['Total Cases_text']),
            totalDeaths=convert_to_int(row['Total Deaths_text']),
            totalRecovered=convert_to_int(row['Total Recovered_text']),
            countryName=row['Country_text'],
            date=DateTime('now'))

    db.commit()


def select_cases(tableName):

    # make a select query and save the result in result
    result = db.execute("SELECT country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date FROM :tableName", tableName=tableName)
    return result


# select query function with condition
def select_cases_where_country(tableName, country):

    result = db.execute("SELECT country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date FROM :tableName WHERE country=:condition", tableName=tableName, condition=country)
    return result


def select_cases_where_country_date(tableName, country, date):

    result = db.execute("SELECT * FROM :tableName WHERE country=:country AND date=:date", tableName=tableName, country=country, date=date)
    return result


def select_unixepoch_date():

    unixepochDate = db.execute("SELECT strftime('%s', 'now')")
    return unixepochDate[0]["strftime('%s', 'now')"]



