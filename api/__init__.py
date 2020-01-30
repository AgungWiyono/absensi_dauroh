from flask import Flask
from flask_restplus import Api

app = Flask(__name__)
api = Api(app, prefix="/api", doc="/doc")

from api.resources import *
