from custom.helpers import *
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
import calendar

def check_registration(db, username, password, confirmation):
    """Take database, username, password and confirmation and return OK if passes every validation, else return error message"""

    # Start assuming that validation is OK
    response = 'OK'
    # If user didn't type one or more information in registration form
    if not username or not password or not confirmation:
        # Set return value to error message
        response = "Please, fill all fields"
    # If password and confirmation don't match
    if password != confirmation:
        # Set return value to error message
        response = "Password and confirmation don't match"
    # If username is already taken
    if db.execute("SELECT username FROM users WHERE username = ?", username):
        # Set return value to error message
        response = "Username already in use"
    # Return response
    return(response)


def check_login(db, username, password):
    """Take database of users, username and password. Return a tuple where:
        If login is valid, first element is True and second element is the user's ID;
        Else first element is False, and second element is proper error message"""

    # Ensure username was submitted
    if not username:
       response = (False, "must provide username")
       return(response)
    # Ensure password was submitted
    elif not password:
        response = (False, "must provide password")
        return(response)
    # Query database for username
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
        response = [False, "invalid username and/or password"]
    else:
        user_id = rows[0]["id"]
        response = (True, user_id)
    return(response)

def get_last_day_of_month(year, monthString):
    month_number = datetime.strptime(monthString, "%B").month
    last_day = calendar.monthrange(year, month_number)[1]
    last_day = datetime.strptime(f'{year}-{monthString}-{last_day}', '%Y-%B-%d').date()
    return(last_day)