# Creation of the application object (of class Flask)
from flask import Flask
app = Flask(__name__)

# Import the 'views.py' module of our application
from grafees import views
