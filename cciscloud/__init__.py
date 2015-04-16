import Queue
from flask import Flask
from flask.ext import restful
from flask.ext.httpauth import HTTPBasicAuth

flaskapp = Flask(__name__)
flaskapi = restful.Api(flaskapp)
flaskauth = HTTPBasicAuth()

ANSIBLE_QUEUE = Queue.Queue()
