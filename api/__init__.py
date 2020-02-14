from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

api = Api(app, prefix="/api", doc="/doc")

from api.resources import *
