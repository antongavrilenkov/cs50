import os
import time

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, timestrftime, Convert


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.filters["strftime"] = timestrftime


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


def add_transaction_to_history(symbol, shares, price, transacted, action):
    '''Add transaction to history'''
    rows = db.execute("INSERT INTO history(user_id, symbol, shares, price, transacted, action) VALUES (:user_id, :symbol, :shares, :price, :transacted, :action)",
                      user_id=session["user_id"], symbol=symbol, shares=shares, price=price, transacted=transacted, action=action)


def get_user_cash():
    user_cash = db.execute("SELECT cash FROM users WHERE id = :id",
                           id=session["user_id"])
    return user_cash[0]["cash"]


def get_users_stocks():
    return db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id",
                      user_id=session["user_id"])


def get_users_stock_by_symbol(symbol):
    users_stocks = get_users_stocks()
    return list(filter(lambda x: x["symbol"] == symbol, users_stocks))[0]


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks_value = 0
    stock_portfolio = []
    users_stocks = get_users_stocks()
    if len(users_stocks) > 0:
        for stock in users_stocks:
            stock_info = lookup(stock["symbol"])
            stock_info["shares"] = stock["shares"]
            stock_total_price = stock_info["price"] * stock["shares"]
            stock_info["total_price"] = stock_total_price
            stocks_value += stock_total_price
            stock_portfolio.append(stock_info)

    cash = get_user_cash()
    total = stocks_value + cash
    return render_template("index.html", **locals())


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Lookup stock info
        symbol = request.form.get("symbol").upper()
        stock_info = lookup(symbol)

        # Check if stock exist
        if stock_info != None:
            new_shares = int(request.form.get("shares"))

            # Check if you have enough cash to buy new stock
            stock_total_price = stock_info["price"] * new_shares
            if stock_total_price <= get_user_cash():
                user_stock = db.execute("SELECT * FROM user_stocks WHERE user_id = :user_id and symbol = :symbol",
                                        user_id=session["user_id"], symbol=symbol)

                # Check if user already have this stock
                if len(user_stock) > 0:
                    user_stock = user_stock[0]
                    if len(user_stock) > 0:
                        db.execute("UPDATE user_stocks SET shares = :shares WHERE user_id = :user_id and symbol = :symbol",
                                   user_id=session["user_id"], symbol=symbol, shares=user_stock["shares"] + new_shares)
                # Create a new stock record in DB
                else:
                    db.execute("INSERT INTO user_stocks(user_id, symbol, shares) VALUES (:user_id, :symbol, :shares)",
                               user_id=session["user_id"], symbol=symbol, shares=new_shares)

                # Add record to history table
                add_transaction_to_history(symbol, new_shares, stock_total_price, time.time(), 'buy')

                # Show success flash message
                flash('Bought!', 'success')

                # Redirect to the home page
                return redirect("/")
            else:
                return apology("can't afford", 400)
        else:
            return apology("Stock not exist", 400)
    else:
        return render_template("buy.html")


@app.route("/add-cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add more cash to user's account"""
    if request.method == "POST":
        amount = int(request.form.get("amount"))
        if amount > 0:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash=get_user_cash() + amount, id=session["user_id"])
            flash('$' + str(amount) + ' added to your account', 'success')
            return redirect("/")
    else:
        return render_template("add-cash.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_records = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY transacted DESC",
                                 user_id=session["user_id"])
    return render_template("history.html", **locals())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # Lookup stock info
        symbol = request.form.get("symbol").upper()
        stock_info = lookup(symbol)

        # Check if stock symbol exists
        if stock_info != None:
            return render_template("quoted.html", **locals())

        else:
            return apology("Stock symbol does not exist", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # Ensure password and confirmation is equal
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("password must be equal to confirmation", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        user_id = None
        # Ensure username not exist
        if len(rows) == 1:
            return apology("Username already exists", 403)

        else:
            rows = db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
                              username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell stock"""
    if request.method == "POST":
        # Lookup stock info
        symbol = request.form.get("symbol").upper()
        users_stock = get_users_stock_by_symbol(symbol)
        stock_info = lookup(symbol)
        shares_to_sell = int(request.form.get("shares"))

        # Check if user owns the stock
        if users_stock["shares"] > 0 and shares_to_sell > 0:

            # Check if you have enough cash to buy new stock
            stock_total_price = stock_info["price"] * shares_to_sell
            if shares_to_sell <= users_stock["shares"]:

                if shares_to_sell == users_stock["shares"]:
                    user_stock = db.execute("DELETE FROM user_stocks WHERE user_id = :user_id and symbol = :symbol",
                                            user_id=session["user_id"], symbol=symbol)
                else:
                    db.execute("UPDATE user_stocks SET shares = :shares WHERE user_id = :user_id and symbol = :symbol",
                               user_id=session["user_id"], symbol=symbol, shares=users_stock["shares"] - shares_to_sell)

                # Add record to history table
                add_transaction_to_history(symbol, shares_to_sell, stock_total_price, time.time(), 'sell')

                # Show success flash message
                flash('Sold!', 'success')

                # Redirect to the home page
                return redirect("/")

            else:
                return apology("You can't sell more than you own", 400)
        else:
            return apology("You don't own the stock", 400)
    else:
        users_stocks = get_users_stocks()
        return render_template("sell.html", **locals())


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
