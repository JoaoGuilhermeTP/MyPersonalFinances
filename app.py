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
    categories = db.execute("SELECT * FROM categories")
    names = [categorie['category_name'] for categorie in categories]
    date = request.form.get('date')
    bank = request.form.get('bank')
    categorie = request.form.get('categorie')
    value = float(request.form.get('value'))
    if not date or not bank or not categorie or not value or categorie not in names:
        return apology("Must fill all fields")
    in_out = db.execute("SELECT in_out FROM categories WHERE category_name = ?", categorie)[0]["in_out"]
    if in_out == "out":
        value = value * -1
    db.execute("INSERT INTO transactions (date, bank, categorie, value, user_id) VALUES (?, ?, ?, ?, ?)", date, bank, categorie, value, session['user_id'])
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
    months = [calendar.month_name[i] for i in range(1,13)]
    if request.method == "GET":
        if request.args.get('year') and request.args.get('month'):
            month = request.args.get('month')
            year = request.args.get('year')
        else:
            today = datetime.now()
            month = today.strftime("%B")
            year = today.strftime("%Y")
    else:
        month = request.form.get("month")
        year = request.form.get("year")
    if not month or not year:
        return apology("Please, fill in every field")
    year = int(year)
    categories = db.execute("SELECT * FROM categories")
    first_day = datetime.strptime(f"{year}-{month}-01", "%Y-%B-%d").date()
    last_day = get_last_day_of_month(year, month)
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? AND date >= ? AND date <= ?", session["user_id"], first_day, last_day)
    for category in categories:
        total = 0
        for transaction in transactions:
            if transaction["categorie"] == category["category_name"]:
                total = total + transaction["value"]
        category["total"] = total
    budgets = db.execute("SELECT * FROM budgets WHERE user_id = ? AND month = ? AND year = ?", session["user_id"], month, year)
    for category in categories:
        for budget in budgets:
            if budget["category_id"] == category["id"]:
                budget["marker"] = True
    return render_template("budget.html", months=months, budgets=budgets, method=request.method, monthSelected=month, yearSelected=year, categories=categories)



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
    if request.method == "GET":
        year = datetime.now().strftime("%Y")
    else:
        year = request.form.get("year")
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
        for budget in budgets:
            if budget['category_id'] == category['id']:
                category['planned'] += budget['planned']
        for transaction in transactions:
            if transaction["categorie"] == category["category_name"]:
                category['total'] += transaction["value"]
    return render_template('reports.html', categories=categories, year=year)



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