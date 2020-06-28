"""
Import modules
"""
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
db = SQL("sqlite:///finance.db")

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


def errorhandler(error_obj):
    """Handle error"""
    if not isinstance(error_obj, HTTPException):
        error_obj = InternalServerError()
    return apology(error_obj.name, error_obj.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
