import sqlite3
from helpers import dict_factory


def select_user(emailAdress):
    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM subscribers WHERE emailAdress="{email}";"""
    sql_command = format_str.format(email=emailAdress)
    cursor.execute(sql_command)
    user = cursor.fetchall()
    # close the connection
    conn.close()
    return user


def insert_user(emailAdress, name, country):
    
    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    format_str = """INSERT INTO subscribers (emailAdress, name, country) VALUES("{email}", "{name}", "{country}");"""
    sql_command = format_str.format(email=emailAdress, name=name, country=country)
    cursor.execute(sql_command)
    conn.commit()
    # close the connection
    conn.close()
    return


def remove_user(emailAdress):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    format_str = """DELETE FROM subscribers WHERE emailAdress="{email}";"""
    sql_command = format_str.format(email=emailAdress)
    cursor.execute(sql_command)
    conn.commit()
    # close the connection
    conn.close()
    return


def select_all_users():

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    sql_command = """SELECT * FROM subscribers"""
    cursor.execute(sql_command)
    users = cursor.fetchall()
    # close the connection
    conn.close()
    return users


def select_all_users_where_country(country):
    
    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM subscribers WHERE country="{country}";"""
    sql_command = format_str.format(country=country)
    cursor.execute(sql_command)
    users = cursor.fetchall()
    # close the connection
    conn.close()
    return users


def update_user(emailAdress, country):

    # Configure SQLite database
    conn = sqlite3.connect('coronaDatabase.db')
    cursor = conn.cursor()
    format_str = """UPDATE subscribers SET country="{country}" WHERE emailAdress="{emailAdress}";"""
    sql_command = format_str.format(country=country, emailAdress=emailAdress)
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

    return