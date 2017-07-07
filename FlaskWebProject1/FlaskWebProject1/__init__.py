"""
The flask application package.
"""

from flask import Flask
from flask_login import login_manager
from flask_oauthlib.client import OAuth
from rauth import OAuth2Service

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object('config.Config')

# Handles the user autentication across the app, for more info: https://flask-login.readthedocs.io/en/latest/ and https://github.com/Vertabelo/flask-oauth-demo-app/blob/master/models.py#L3
lm = login_manager.LoginManager()
lm.init_app(app)
lm.login_view = 'index'

import FlaskWebProject1.views
