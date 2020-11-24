import sqlite3
from helpers import dict_factory, connect_to_db


def select_user(tableName, emailAdress):

    # Configure SQLite database
    conn = connect_to_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM "{table}" WHERE emailAdress="{email}";"""
    sql_command = format_str.format(table=tableName, email=emailAdress)
    cursor.execute(sql_command)
    user = cursor.fetchall()
    # close the connection
    conn.close()
    return user


def select_user_where_email(tableName, emailAdress):

    # Configure SQLite database
    conn = connect_to_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM "{table}" WHERE emailAdress="{email}";"""
    sql_command = format_str.format(table=tableName, email=emailAdress)
    cursor.execute(sql_command)
    user = cursor.fetchall()
    # close the connection
    conn.close()
    return user


def select_user_where_userID(tableName, userID):

    # Configure SQLite database
    conn = connect_to_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM "{table}" WHERE user_id="{userID}";"""
    sql_command = format_str.format(table=tableName, userID=userID)
    cursor.execute(sql_command)
    user = cursor.fetchall()
    # close the connection
    conn.close()
    return user



def insert_user(emailAdress, name, country):
    
    # Configure SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()
    format_str = """INSERT INTO subscribers (emailAdress, name, country) VALUES("{email}", "{name}", "{country}");"""
    sql_command = format_str.format(email=emailAdress, name=name, country=country)
    cursor.execute(sql_command)
    conn.commit()
    # close the connection
    conn.close()
    return


def isert_user_into_users(tableName, emailAddress, name, hashPsw, role):

    # Configure SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()
    format_str = """INSERT INTO "{table}" (emailAdress, name, hash, role) VALUES("{email}", "{name}", "{hash}", "{role}");"""
    sql_command = format_str.format(table=tableName, email=emailAddress, name=name, hash=hashPsw, role=role)
    cursor.execute(sql_command)
    conn.commit()
    # close the connection
    conn.close()
    return


def remove_user(emailAdress):

    # Configure SQLite database
    conn = connect_to_db()
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
    conn = connect_to_db()
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
    conn = connect_to_db()
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    format_str = """SELECT * FROM subscribers WHERE country="{country}";"""
    sql_command = format_str.format(country=country)
    cursor.execute(sql_command)
    users = cursor.fetchall()
    # close the connection
    conn.close()
    return users


def update_user(userID, country):

    # Configure SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()
    format_str = """UPDATE subscribers SET country="{country}" WHERE subscriber_id="{userID}";"""
    sql_command = format_str.format(country=country, userID=userID)
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

    return


def update_name_country(userID, country, name):

    # Configure SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()
    format_str = """UPDATE subscribers SET country="{country}", Name="{name}" WHERE subscriber_id="{userID}";"""
    sql_command = format_str.format(country=country, name=name, userID=userID)
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

    return


def delete_where_userID(userID):

    # Configure SQLite database
    conn = connect_to_db()
    cursor = conn.cursor()
    format_str = """DELETE FROM subscribers WHERE subscriber_id="{userID}";"""
    sql_command = format_str.format(userID=userID)
    cursor.execute(sql_command)
    conn.commit()
    conn.close()

    return