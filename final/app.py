"""
Import modules
"""
import shutil
from flask import Flask, render_template, request, send_file
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from generator import generator

from helpers import apology

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


def errorhandler(error_obj):
    """Handle error"""
    if not isinstance(error_obj, HTTPException):
        error_obj = InternalServerError()
    return apology(error_obj.name, error_obj.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
