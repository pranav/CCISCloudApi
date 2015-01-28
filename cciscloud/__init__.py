from flask import Flask
from flask.ext import restful

flaskapp = Flask(__name__)
flaskapi = restful.Api(flaskapp)
