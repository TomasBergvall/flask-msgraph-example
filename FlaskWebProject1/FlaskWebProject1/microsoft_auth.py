from flask import current_app, redirect, url_for, request, session
from rauth import OAuth2Service
import uuid
import json


class MicrosoftSignIn(object):

    def __init__(self):
        self.consumer_id = current_app.config['MS_CLIENT_ID']
        self.consumer_secret = current_app.config['MS_CLIENT_SECRET']

        self.service = OAuth2Service(
            name='microsoft',
            client_id=current_app.config['MS_CLIENT_ID'],
            client_secret=current_app.config['MS_CLIENT_SECRET'],
            authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
            access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
            base_url='https://graph.microsoft.com/v1.0/'
        )


    def get_callback_url(self):
        return url_for('authorized', _external=True)

    def authorize(self):
        guid = uuid.uuid4() # guid used to only accept initiated logins
        session['state'] = guid
        return redirect(self.service.get_authorize_url(
            #scope='openid',
            scope='user.read',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None, None

        data={'code': request.args['code'],
                      'grant_type': 'authorization_code',
                      'redirect_uri': self.get_callback_url()}

        # --------------------------------------------------------
        # I had some problems with self.service.get_auth_session(data=data , decoder=json.loads)
        # This at least worked but need further work to be completed if the function above stops working.
        # --------------------------------------------------------
        #response = self.service.get_raw_access_token(data=data)
        #response = response.json()    
        #oauth2_session = self.service.get_session(response['access_token'])
        #user = self.service.get('https://graph.microsoft.com/v1.0/me').json()


        oauth_session = self.service.get_auth_session(data=data , decoder=json.loads)

        # okay to store this in a local variable, encrypt if it's going to client
        # machine or database. treat as a password.
        session['microsoft_token'] = (oauth_session.access_token, '')
        # store the token in another session variable for easy access
        session['access_token'] = oauth_session.access_token
        
        me = oauth_session.get('me').json()
        return {'id': me['id'],
                'external_authorizer': 'microsoft',
                'email': me.get('mail'),
                'first_name': me.get('givenName'),
                'last_name': me.get('surname')
                }
            
        

