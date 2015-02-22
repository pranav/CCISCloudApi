import cciscloud
from cciscloud.api.condense import CondenseApi
from cciscloud.api.instance import InstanceApi
from cciscloud.api.user import UserCostApi
app = cciscloud.flaskapp


cciscloud.flaskapi.add_resource(InstanceApi, '/api/v1/instance/<string:identifier>')
cciscloud.flaskapi.add_resource(UserCostApi, '/api/v1/user/<string:user>/cost')


if __name__ == '__main__':
    cciscloud.flaskapp.run(debug=True)
