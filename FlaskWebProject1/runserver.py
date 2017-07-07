"""
This script runs the FlaskWebProject1 application using a development server.
"""

from os import environ
from FlaskWebProject1 import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    
    # Port needs to be specified at https://apps.dev.microsoft.com/ in order to work, hence can't change
    app.run(HOST, 5000)
