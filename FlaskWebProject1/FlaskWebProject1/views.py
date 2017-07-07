"""
Routes and views for the flask application.
"""
# Import app = the application and lm = the login manager
# Used e.g. when decorating the routing functions.
from FlaskWebProject1 import app, lm

from models import UserProfile, AccessControl, WebApplication, db
from microsoft_auth import MicrosoftSignIn


from flask import Flask, redirect, url_for, session, request, render_template, g, current_app
from flask_oauthlib.client import OAuth
from flask_login import (
    login_user, 
    logout_user, 
    login_required, 
    current_user
)
import uuid
import json
from datetime import datetime
import requests

@lm.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
#requests.packages.urllib3.disable_warnings()

@app.route('/')
def index():
    """Handler for home page."""
    if(current_user.is_authenticated):
        return redirect('home')
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
@login_required
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
@login_required
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/login')
def login():
    """handler for login route."""
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    ms_oauth = MicrosoftSignIn()
    return ms_oauth.authorize()

@app.route('/logout')
@login_required
def logout():
    """handler for logout route."""
    session.pop('microsoft_token', None)
    session.pop('state', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    """handler for login/authorized route."""
    ms_oauth = MicrosoftSignIn()
    response = ms_oauth.callback()

    if response is None:
        return "access denied: reason={0}\nerror={1}".format( \
            request.args['error'], request.args['error_description'])

    # check response for state
    #if str(session['state']) != str(request.args['state']):
    #    raise exception('state has been messed with, end authentication')
    #session['state'] = '' # reset session state to prevent re-use

    # retrieve the user data from the database
    user = UserProfile.query.filter_by(external_id=response['id'], external_authorizer='microsoft').first()

    # if the user is new, we store theirs credentials in user_profile table
    if not user:
        user = UserProfile(external_id=response['id'], external_authorizer=response['external_authorizer'], email=response['email'], first_name=response['first_name'], last_name=response['last_name'])
        db.session.add(user)
        db.session.commit()
    
    # Check if user is allowed to access this application
    q = db.session.query(UserProfile,WebApplication,AccessControl).\
        filter(UserProfile.id == AccessControl.user_id).\
        filter(WebApplication.web_application_id == AccessControl.web_application_id).\
        filter(UserProfile.id == user.id).\
        filter(WebApplication.web_application_name == app.config['APPLICATION_NAME']).first()

    # Only login user if value is found in AccessControl 
    if(q is not None):
        # TODO: Alert user that they are not authorized to access this application
        login_user(user)

    return redirect('home')

















