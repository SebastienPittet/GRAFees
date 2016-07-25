# Creation of the application object (of class Flask)
from flask import Flask
app = Flask(__name__)

# Configuration (http://flask.pocoo.org/docs/0.11/config/#configuring-from-files)
app.config.from_object('grafees.config') # load config from module
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')

# Import the 'views.py' module of our application
from grafees import views
