from flask import request
from cciscloud.api import CCISCloudApi
from cciscloud.models.user import User


class UserCostApi(CCISCloudApi):

    def get(self, user):
        return {
            'total_cost': User(user).total_cost,
            'user': user
        }


class WhoAmIApi(CCISCloudApi):

    def get(self):
        return {'username': request.authorization.username}
