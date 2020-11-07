from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///coronaDatabase.db")


def select_user(emailAdress):

    user = db.execute("SELECT * from subscribers WHERE emailAdress=:email", email=emailAdress)
    return user

def insert_user(emailAdress, name, country):

    db.execute("INSERT INTO subscribers(emailAdress, name, country) VALUES(:email, :name, :country)",
            email=emailAdress, name=name, country=country)
    return

def remove_user(emailAdress):

    db.execute("DELETE FROM subscribers WHERE emailAdress=:email", email=emailAdress)
    return

def select_all_users():

    users = db.execute("SELECT * FROM subscribers")
    return users