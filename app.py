# Import modules
import calendar
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash
from custom.helpers import *
from custom.custom import *

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finances.db")


# LOGIN ------------------------------------------------------------------------------------------
@app.route("/login", methods=["POST", "GET"])
def login():
    # Forget any user_id
    session.clear()
    # If user clicked login button (POST)
    if request.method == "POST":
        # Get info entered by user
        username = request.form.get('username')
        password = request.form.get('password')
        # Validate login with custom function check_login()
        response = check_login(db, username, password)
        # If passed login check
        if response[0]:
            # Remember which user has logged in
            session["user_id"] = response[1]
            session["username"] = username
            # Redirect user to home page
            return redirect("/")
        # If not passed login check
        else:
            return apology(response[1], 403)
    # User got here by GET method
    else:
        # Show file login.html
        return render_template("login.html")


# REGISTER ------------------------------------------------------------------------------------------
@app.route("/register", methods=["POST", "GET"])
def register():
    # If user is not accessing route via form
    if request.method == "GET":
        # Show file register.html
        return render_template("register.html")
    # Get info typed by user in registration form
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    # Validate registration with custom function check_registration()
    response = check_registration(db, username, password, confirmation)
    # If didn't pass validation
    if response != 'OK':
        # Show error message
        return apology(response, 403)
    # Else if passed validation
    else:
        # Insert new user in database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        # Redirect to login page
        return redirect("/login")


# INDEX ------------------------------------------------------------------------------------------
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    # Get transactions made by current user from database and store in dictionary "transactions"
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC", session['user_id'])
    # Get bank names from database and store in dictionary "banks"
    banks = db.execute("SELECT bank_name FROM banks")
    # Get categories info from database and store in dictionary "categories"
    categories = db.execute("SELECT * FROM categories")
    # Create new blank set for banks
    current_banks = set()
    # Create new blank set for categories
    current_categories = set()
    # For each item in transactions dictionary
    for transaction in transactions:
        current_banks.add(transaction["bank"])
        current_categories.add(transaction["categorie"])
    # Get values from filter form
    filt = {
        "start_date" : request.form.get("start_date"),
        "end_date" : request.form.get("end_date"),
        "filter_bank" : request.form.get("filter_bank"),
        "filter_category" : request.form.get("filter_category")
    }

    # If user is trying filter with start date bigger than end date, return error
    if (filt["start_date"] and filt["end_date"]) and filt["start_date"] > filt["end_date"]:
        return apology("Start date can't be after end date")

    return render_template("transactions.html",
                            transactions=transactions,
                            banks=banks,
                            current_banks=current_banks,
                            current_categories=current_categories,
                            categories=categories,
                            filt=filt)



@app.route("/add_transaction", methods=['POST'])
@login_required
def add_transaction():

    # Get categories from database and store in dictionary
    categories = db.execute("SELECT * FROM categories")

    # Get values informed by user when adding the transaction
    date = request.form.get('date')
    bank = request.form.get('bank')
    categorie_name = request.form.get('categorie')
    value = float(request.form.get('value'))

    # Check if every field was filled
    if not date or not bank or not categorie_name or not value:
        return apology("Must fill all fields")

    # Check if category name is in database
    names = [category['category_name'] for category in categories]
    if categorie_name not in names:
        return apology("Not a valid category")

    # Figure out if the value should be positive or negative, based on the category "in_out" field
    in_out = db.execute("SELECT in_out FROM categories WHERE category_name = ?", categorie_name)[0]["in_out"]
    if (in_out == "out" and value > 0) or (in_out == "in" and value < 0):
        value = value * -1

    # Insert transaction into database
    db.execute("INSERT INTO transactions (date, bank, categorie, value, user_id) VALUES (?, ?, ?, ?, ?)", date, bank, categorie_name, value, session['user_id'])

    # Redirect to root
    return redirect('/')



@app.route("/deleteAll", methods=['POST'])
@login_required
def deleteAll():
    db.execute("DELETE FROM transactions WHERE user_id = ?", session["user_id"])
    return redirect('/')



@app.route("/delete_transaction", methods=['POST'])
@login_required
def delete_transaction():
    transaction_id = int(request.form.get('transaction_id'))
    db.execute("DELETE FROM transactions WHERE id = ?", transaction_id)
    return redirect('/')



@app.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    filt = False
    # First, get a list containing all the months in a year
    months = [calendar.month_name[i] for i in range(1,13)]

    # The variables month, year amd filt will be set according to the request method

    # If the request method is GET
    if request.method == "GET":

        # If user was redirected via GET from the /addBudget route with month and year as arguments, meaning they have changed some budget, set year and month to wathever was previously in the form
        if request.args.get('year') and request.args.get('month'):
            month = request.args.get('month')
            year = request.args.get('year')

        # Else if they are accessing this route from scracth, set month and year to the current date
        else:
            today = datetime.now()
            month = today.strftime("%B")
            year = today.strftime("%Y")

    # Else if the request method is POST, set month and year to whatever the user inputed via form, ad get wether user checked the filter checkbox
    elif request.method == "POST":
        month = request.form.get("month")
        year = request.form.get("year")
        filt = request.form.get("filter")

        # Check if user has filled the form correctly
        if not month or not year:
            return apology("Please, fill in every field")

    # The following lines will be executed wether the method was POST or GET, if the function didn't return yet duo to missfilling the form

    # Make year into an integer
    year = int(year)

    # Get first day and last day of the month
    first_day = datetime.strptime(f"{year}-{month}-01", "%Y-%B-%d").date()
    last_day = get_last_day_of_month(year, month)

    # Get categories from database and store as dictionary
    categories = db.execute("SELECT * FROM categories")

    # Get transactions and budgets from database and store as dictionary, filtering by user id, first day and last day of the month
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? AND date >= ? AND date <= ?", session["user_id"], first_day, last_day)

    # Get budgets from database and store as dictionary, filtering by user id, month and year
    budgets = db.execute("SELECT * FROM budgets WHERE user_id = ? AND month = ? AND year = ?", session["user_id"], month, year)

    # For each category in categories dictionary
    for category in categories:

        # Create key-value pair to decide whether the categorie whould be shown or not. Initialize with the value of True, meaning it should show.
        category["show"] = True
        category["budget"] = False

        #Create a Key called "total" with the value of 0
        category["total"] = 0

        # For each transaction in the transactions dictionary
        for transaction in transactions:

            # Transaction name corresponds to category name, update the value for the "total" key
            if transaction["categorie"] == category["category_name"]:
                category["total"] += transaction["value"]

        # For each budget, check if the category_id for this budget corresponts with current categories' id. If it does, it means there is a budget for that category.
        # A new key with the value of True will be added to this budget. This will be used in the HTML file to know when to show a budget of a blank input field
        for budget in budgets:
            if budget["category_id"] == category["id"]:
                budget["marker"] = True
                category["budget"] = True

        if filt:
            if not category["budget"] and category["total"] == 0:
                category["show"] = False

    # Renter budget.html template, passing necessary variables
    return render_template("budget.html", months=months, budgets=budgets, method=request.method, monthSelected=month, yearSelected=year, categories=categories, filt=filt)



@app.route("/addBudget", methods=["POST"])
@login_required
def addBudget():
    """Add and update budget"""

    # Get categories info from database and store in dictionary
    categories = db.execute("SELECT * FROM categories")
    # Get info for month and year from form
    month = request.form.get("month")
    year = int(request.form.get("year"))
    # For each category in dictionary
    for category in categories:
        # Get ammount planned for that category from form
        planned = request.form.get(f"planned_{category['id']}")
        # If user typed a value that is not zero
        if planned and float(planned) != 0:
            # Transform value into a float
            planned = float(planned)
            # Make value negative if it refers to outgoin money and positive if it's incoming money
            if category['in_out'] == 'out' and planned > 0:
                planned *= -1
            if category['in_out'] == 'in' and planned < 0:
                planned *= -1
            # Update value if there was already a previous one, and inserting new value if there wasn't
            if db.execute("SELECT * FROM budgets WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?", session["user_id"], category['id'], month, year):
                db.execute("UPDATE budgets SET planned = ? WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?", planned, session["user_id"], category['id'], month, year)
            else:
                db.execute("INSERT INTO budgets (user_id, category_id, month, year, planned) VALUES (?, ?, ?, ?, ?)", session["user_id"], category['id'], month, year, planned)
        # Delete value if user left it blank of set to zero
        else:
            db.execute("DELETE FROM budgets WHERE (user_id = ? AND category_id = ? AND month = ? AND year = ?)", session["user_id"], category['id'], month, year)
    # Redirect to "/budget" route passing values for year and month
    return redirect(url_for("budget", year=year, month=month))



@app.route("/reports", methods=["GET", "POST"])
@login_required
def reports():
    filt = False
    if request.method == "GET":
        year = datetime.now().strftime("%Y")
    else:
        year = request.form.get("year")
        filt = request.form.get("filter")
    if not year:
        return apology("Please, fill in every field")
    year = int(year)
    first_day = datetime.strptime(f"{year}-{'January'}-01", "%Y-%B-%d").date()
    last_day = datetime.strptime(f"{year}-{'December'}-31", "%Y-%B-%d").date()
    categories = db.execute("SELECT * FROM categories")
    budgets = db.execute("SELECT * FROM budgets WHERE user_id = ? AND year = ?", session['user_id'], year)
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? AND date >= ? AND date <= ?", session["user_id"], first_day, last_day)
    for category in categories:
        category['planned'] = 0
        category['total'] = 0
        category['show'] = True
        for budget in budgets:
            if budget['category_id'] == category['id']:
                category['planned'] += budget['planned']
        for transaction in transactions:
            if transaction["categorie"] == category["category_name"]:
                category['total'] += transaction["value"]
        if filt:
            if category['planned'] == 0 and category['total'] == 0:
                category['show'] = False
    return render_template('reports.html', categories=categories, year=year, filt=filt)



@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")

@app.route("/deleteAccount")
@login_required
def deleteAccount():
    """Delete User Account"""
    db.execute("DELETE FROM users WHERE id = ?", session['user_id'])
    db.execute("DELETE FROM transactions WHERE user_id = ?", session['user_id'])
    db.execute("DELETE FROM budgets WHERE user_id = ?", session['user_id'])
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")