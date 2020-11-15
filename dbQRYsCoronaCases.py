from helpers import get_API_News_austria, get_API_News_world, convert_to_int, dict_factory
from datetime import date
from send import email_to_subscribers
from contextlib import closing
import http.client
import json
import sqlite3


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
    print(tblValues)
    if bool(tblValues):
        # compare the values from table with the values from API
        if tblValues[0]['totalCases'] == convert_to_int(APIData[0]['Total Cases_text']):
            return
        else:
            update_query_world(APIData)
            # if new data, insert it into history
            #insert_into_history(APIData)
            # send an email to subscribers
            email_to_subscribers()
    else:
        insert_query(APIData)
        email_to_subscribers()
        #insert_into_history(APIData)


def insert_query(APIData):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    currDate = get_date()
    # for each row in APIData
    for row in APIData:
        # many key errors from API. solve the problems with a try block
        try:
            format_str = """INSERT INTO casesWorld
                            (country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date)
                            VALUES("{countryName}", "{activeCases}", "{newCases}", "{newDeaths}", "{totalCases}", "{totalDeaths}", "{totalRecovered}", "{date}");"""

            sql_command = format_str.format(countryName=row['Country_text'], activeCases=convert_to_int(row['Active Cases_text']), 
                                            newCases=convert_to_int(row['New Cases_text']), newDeaths=convert_to_int(row['New Deaths_text']),
                                            totalCases=convert_to_int(row['Total Cases_text']), totalDeaths=convert_to_int(row['Total Deaths_text']),
                                            totalRecovered=convert_to_int(row['Total Recovered_text']), date=currDate)
            cursor.execute(sql_command)
        except KeyError:
            continue
    conn.commit()
    # close the connection
    conn.close()


def insert_into_history(APIData):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    today = date.today()
    tblHistory = "history"
    todayValues = {}

    # for each row in APIData
    for row in APIData:
        # many key errors. solve the problems with try block
        try:
            # get the values from current date
            todayValues = select_cases_where_country_date(tblHistory, row['Country_text'], today)
        except KeyError:
            continue
        
        """
        check if today date for current country is already in the database
        if not, insert the data of the current date
        """ 
        if bool(todayValues):
            continue
        else:
            try:
                format_str = """INSERT INTO history
                                (country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date)
                                VALUES("{countryName}", "{activeCases}", "{newCases}", "{newDeaths}", "{totalCases}", "{totalDeaths}", "{totalRecovered}", "{date}");"""                
                sql_command = format_str.format(countryName=row['Country_text'], activeCases=convert_to_int(row['Active Cases_text']), 
                                                newCases=convert_to_int(row['New Cases_text']), newDeaths=convert_to_int(row['New Deaths_text']),
                                                totalCases=convert_to_int(row['Total Cases_text']), totalDeaths=convert_to_int(row['Total Deaths_text']),
                                                totalRecovered=convert_to_int(row['Total Recovered_text']), date=today)
                cursor.execute(sql_command)
            except KeyError:
                continue

    # commit the changes
    conn.commit()
    # close the connection
    conn.close()


def update_query_world(APIData):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    currDate = get_date()
    
    for row in APIData:
        try:
            format_str = """UPDATE casesWorld 
                            SET active="{activeCases}",
                            new="{newCases}",
                            deaths="{newDeaths}",
                            totalCases="{totalCases}",
                            totalDeaths="{totalDeaths}",
                            totalRecovered="{totalRecovered}",
                            date="{lastUpdate}" WHERE country="{countryName}";"""
            
            sql_command = format_str.format(countryName=row['Country_text'], activeCases=convert_to_int(row['Active Cases_text']),
                                            newCases=convert_to_int(row['New Cases_text']), newDeaths=convert_to_int(row['New Deaths_text']),
                                            totalCases=convert_to_int(row['Total Cases_text']), totalDeaths=convert_to_int(row['Total Deaths_text']),
                                            totalRecovered=convert_to_int(row['Total Recovered_text']), lastUpdate=currDate)
            cursor.execute(sql_command)
        except KeyError:
            continue
    conn.commit()
    # close the connection
    conn.close()    


def select_cases(tableName):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date FROM "{table}";"""
    sql_command = format_str.format(table=tableName)
    cursor.execute(sql_command)
    result = cursor.fetchall()
    # make a select query and save the result in result
    #result = cursor.execute("SELECT country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date FROM :tableName", {"tableName": tableName}).fetchall()
    
    # close the connection
    conn.close()

    return result


# select query function with condition
def select_cases_where_country(tableName, country):
    
    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT country, active, new, deaths, totalCases, totalDeaths, totalRecovered, date FROM "{table}" WHERE country="{countryName}";"""
    sql_command = format_str.format(table=tableName, countryName=country)
    cursor.execute(sql_command)
    result = cursor.fetchall()
    
    # close the connection
    conn.close()
    return result


def select_cases_where_country_date(tableName, country, date):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM "{table}" WHERE country="{countryName}" AND date="{dateUnix}";"""
    sql_command = format_str.format(table=tableName, countryName=country, dateUnix=date)
    cursor.execute(sql_command)
    #result = cursor.execute("SELECT * FROM :tableName WHERE country=:country AND date=:date", {"tableName": tableName, "country": country, "date": date}).fetchall()
    result = cursor.fetchall()
    # close the connection
    conn.close()

    return result


def get_date():
    today = date.today()
    return today

