from flask import Blueprint

auth = Blueprint('auth', __name__)


#Login Page
@auth.route('/login')
def login():
    return "<p>Login<p>"

#Logout page
@auth.route('/logout')
def logout():
    return "<p>Logout<p>"
#Signup page
@auth.route('/signup')
def signup():
    return "<p>Signup<p>"
