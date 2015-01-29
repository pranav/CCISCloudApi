from cciscloud.models.user import User
from flask.ext.restful import reqparse, Resource


class UserCostApi(Resource):
    def get(self, user):
        return {
            'total_cost': User(user).total_cost,
            'user': user
        }
