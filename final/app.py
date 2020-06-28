"""
Import modules
"""
from cs50 import SQL
import shutil
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from generator import generator
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, timestrftime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    '''Add headers to response headers'''
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///slideshows.db")

@app.route("/", methods=["GET", "POST"])
def index():
    """Show portfolio of stocks"""
    if request.method == "POST":
        texts = request.form.getlist("text[]")
        text_colors = request.form.getlist("text_color[]")
        bg_colors = request.form.getlist("bg_color[]")
        video_format = request.form.getlist("video_format")
        bg_music = request.form.getlist("bg_music")
        slide_duration = request.form.getlist("slide_duration")

        file_path = app.root_path + '/' + \
                    generator({'texts': texts, 'text_colors': text_colors,
                               'bg_colors': bg_colors, 'video_format': video_format[0],
                               'bg_music': bg_music[0], 'slide_duration': slide_duration[0]})
        file_handle = open(file_path, 'r')
        try:
            @app.after_request
            def remove_file(response):
                '''Delete temp folder and all files in temp folder'''
                try:
                    shutil.rmtree('static/temp')
                    file_handle.close()
                except Exception as error:
                    print("Error removing or closing downloaded file handle", error)
                return response
            return send_file(file_path, as_attachment=True, mimetype='video/mp4',
                             attachment_filename='slides.mp4')
        except Exception as exception_obj:
            print(str(exception_obj))
    else:
        return render_template("index.html", **locals())


@app.route("/slideshows")
@login_required
def history():
    """Show history of transactions"""
    history_records = db.execute("SELECT * FROM history WHERE user_id = :user_id ORDER BY transacted DESC",
                                 user_id=session["user_id"])
    return render_template("slideshows.html", **locals())


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


def errorhandler(error_obj):
    """Handle error"""
    if not isinstance(error_obj, HTTPException):
        error_obj = InternalServerError()
    return apology(error_obj.name, error_obj.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
