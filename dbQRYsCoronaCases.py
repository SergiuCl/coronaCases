from cs50 import SQL
from helpers import get_API_News_austria, get_API_News_world
from datetime import date
from send import email_to_subscribers
import http.client
import json



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///coronaDatabase.db")

# define global variables
notAvailable = "N/A"
keyLastUpdate = "Last Update"


def get_cases_austria():

    # load the data in JSON
    casesAustria = get_API_News_austria()
    
    # call the function to update table
    update_cases_austria(casesAustria)



def get_cases_world():

    # load the data in JSON
    casesWorld = get_API_News_world()
    # call the function to update the table
    update_cases_world(casesWorld)
    


def update_cases_austria(APIData):

    tblValues = {}
    tblCasesInAustria = "casesInAustria"

    # get the values from table
    tblValues = select_cases(tblCasesInAustria) 

    """
    ensure dict is not None
    if the value did not change, exit function
    else, update the table
    """ 
    if bool(tblValues):
        if tblValues[0]['totalCases'] == APIData['Total Cases_text']:
            return
        else:
            # update the table casesInAustria
            update_query_austria(APIData)
    else:
        insert_query_austria(APIData)

    
    


def update_cases_world(APIData):
    tblCasesWorld = "casesWorld"
    # get the values from table, WHERE country is "world" - that means the total number of cases
    condition = "World"
    tblValues = select_cases_where_country(tblCasesWorld, condition)
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
            insert_into_history(APIData)
            # send an email to subscribers
            email_to_subscribers()
    else:
        insert_query(APIData)
        insert_into_history(APIData)


def update_query_austria(APIData):
    
    # for each row in APIData
    # ensure key 'Last Update' exists in dict
    # if exists - insert all the values into the table casesWorld
    # if not - insert N/A into 'Last Update'
    if keyLastUpdate in APIData:
        db.execute("""UPDATE casesInAustria
                        SET activeCases = :activeCases, 
                        newCases = :newCases, 
                        newDeaths = :newDeaths, 
                        totalCases = :totalCases, 
                        totalDeaths = :totalDeaths, 
                        totalRecovered = :totalRecovered, 
                        lastUpdate = :lastUpdate""",

            activeCases=APIData['Active Cases_text'], 
            newCases=APIData['New Cases_text'], 
            newDeaths=APIData['New Deaths_text'], 
            totalCases=APIData['Total Cases_text'], 
            totalDeaths=APIData['Total Deaths_text'], 
            totalRecovered=APIData['Total Recovered_text'], 
            lastUpdate=APIData['Last Update'])
    else:
        db.execute("""UPDATE casesInAustria
                        SET activeCases = :activeCases, 
                        newCases = :newCases, 
                        newDeaths = :newDeaths, 
                        totalCases = :totalCases, 
                        totalDeaths = :totalDeaths, 
                        totalRecovered = :totalRecovered, 
                        lastUpdate = :lastUpdate""",

            activeCases=APIData['Active Cases_text'], 
            newCases=APIData['New Cases_text'], 
            newDeaths=APIData['New Deaths_text'], 
            totalCases=APIData['Total Cases_text'], 
            totalDeaths=APIData['Total Deaths_text'], 
            totalRecovered=APIData['Total Recovered_text'], 
            lastUpdate=notAvailable)



def insert_query(APIData):

    # for each row in APIData
    # ensure key 'Last Update' exists in dict
    # if exists - insert all the values into the table casesWorld
    # if not - insert N/A into 'Last Update'
    for row in APIData:
        if keyLastUpdate in APIData:
            db.execute("""INSERT INTO casesWorld
                            (country, activeCases, newCases, newDeaths, totalCases, totalDeaths, totalRecovered, lastUpdate)
                            VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :lastUpdate)""",
                    
                countryName=row['Country_text'],
                activeCases=row['Active Cases_text'],
                newCases=row['New Cases_text'],
                newDeaths=row['New Deaths_text'],
                totalCases=row['Total Cases_text'],
                totalDeaths=row['Total Deaths_text'],
                totalRecovered=row['Total Recovered_text'],
                lastUpdate=row['Last Update'])
        else:
            db.execute("""INSERT INTO casesWorld
                            (country, activeCases, newCases, newDeaths, totalCases, totalDeaths, totalRecovered, lastUpdate)
                            VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :lastUpdate)""",
                                
                countryName=row['Country_text'],
                activeCases=row['Active Cases_text'],
                newCases=row['New Cases_text'],
                newDeaths=row['New Deaths_text'],
                totalCases=row['Total Cases_text'],
                totalDeaths=row['Total Deaths_text'],
                totalRecovered=row['Total Recovered_text'],
                lastUpdate=notAvailable)
    db.commit()
    # send an email to subscribers
    #email_to_subscribers(APIData[0]['Total Cases_text'], APIData[0]['New Cases_text'])
    email_to_subscribers()

def insert_query_austria(APIData):

    # for each row in APIData
    # ensure key 'Last Update' exists in dict
    # if exists - insert all the values into the table casesWorld
    # if not - insert N/A into 'Last Update'
    if keyLastUpdate in APIData:
        db.execute("""INSERT INTO casesInAustria
                        (country, activeCases, newCases, newDeaths, totalCases, totalDeaths, totalRecovered, lastUpdate)
                        VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :lastUpdate)""",

            countryName=APIData['Country_text'], 
            activeCases=APIData['Active Cases_text'],
            newCases=APIData['New Cases_text'],
            newDeaths=APIData['New Deaths_text'],
            totalCases=APIData['Total Cases_text'],
            totalDeaths=APIData['Total Deaths_text'],
            totalRecovered=APIData['Total Recovered_text'],
            lastUpdate=APIData['Last Update'])
    else:
        db.execute("""INSERT INTO casesInAustria
                        (country, activeCases, newCases, newDeaths, totalCases, totalDeaths, totalRecovered, lastUpdate)
                        VALUES(:countryName, :activeCases, :newCases, :newDeaths, :totalCases, :totalDeaths, :totalRecovered, :lastUpdate)""",

            countryName=APIData['Country_text'], 
            activeCases=APIData['Active Cases_text'],
            newCases=APIData['New Cases_text'],
            newDeaths=APIData['New Deaths_text'],
            totalCases=APIData['Total Cases_text'],
            totalDeaths=APIData['Total Deaths_text'],
            totalRecovered=APIData['Total Recovered_text'],
            lastUpdate=notAvailable)


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

'''
def update_tblHistory(tblName, APIData, date):

    db.execute("""UPDATE :tblName
                    SET activeCases = :activeCases, 
                    newCases = :newCases, 
                    newDeaths = :newDeaths, 
                    totalCases = :totalCases, 
                    totalDeaths = :totalDeaths, 
                    totalRecovered = :totalRecovered
                    date = :date
                    WHERE country=:country AND date=:date""",

                tblName=tblName,
                activeCases=APIData['Active Cases_text'], 
                newCases=APIData['New Cases_text'], 
                newDeaths=APIData['New Deaths_text'], 
                totalCases=APIData['Total Cases_text'], 
                totalDeaths=APIData['Total Deaths_text'], 
                totalRecovered=APIData['Total Recovered_text'],
                country=APIData['Country_text'],
                date=date)
'''

def update_query_world(APIData):

    for row in APIData:
        if keyLastUpdate in row:
            db.execute("""UPDATE casesWorld
                            SET activeCases = :activeCases,
                            newCases = :newCases,
                            newDeaths = :newDeaths,
                            totalCases = :totalCases,
                            totalDeaths = :totalDeaths,
                            totalRecovered = :totalRecovered,
                            lastUpdate = :lastUpdate
                            WHERE country= :countryName""",
                
                activeCases=row['Active Cases_text'],
                newCases=row['New Cases_text'],
                newDeaths=row['New Deaths_text'],
                totalCases=row['Total Cases_text'],
                totalDeaths=row['Total Deaths_text'],
                totalRecovered=row['Total Recovered_text'],
                lastUpdate=row['Last Update'],
                countryName=row['Country_text'])
        else:
            db.execute("""UPDATE casesWorld
                            SET activeCases = :activeCases,
                            newCases = :newCases,
                            newDeaths = :newDeaths,
                            totalCases = :totalCases,
                            totalDeaths = :totalDeaths,
                            totalRecovered = :totalRecovered,
                            lastUpdate = :lastUpdate
                            WHERE country= :countryName""",
                
                activeCases=row['Active Cases_text'],
                newCases=row['New Cases_text'],
                newDeaths=row['New Deaths_text'],
                totalCases=row['Total Cases_text'],
                totalDeaths=row['Total Deaths_text'],
                totalRecovered=row['Total Recovered_text'],
                lastUpdate=notAvailable,
                countryName=row['Country_text'])
    db.commit()


def select_cases(tableName):

    # make a select query and save the result in result
    result = db.execute("SELECT * FROM :tableName", tableName=tableName)
    return result


# select query function with condition
def select_cases_where_country(tableName, country):

    result = db.execute("SELECT * FROM :tableName WHERE country=:condition", tableName=tableName, condition=country)
    return result


def select_cases_where_country_date(tableName, country, date):

    result = db.execute("SELECT * FROM :tableName WHERE country=:country AND date=:date", tableName=tableName, country=country, date=date)
    return result
