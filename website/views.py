from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #calls home() function
def home():
    return render_template("home.html")
