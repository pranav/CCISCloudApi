from flask.ext.restful import Resource
from cciscloud.auth import requires_auth

class CCISCloudApi(Resource):
    method_decorators = [requires_auth]