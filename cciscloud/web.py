import cciscloud
from cciscloud.api.condense import CondenseApi
from cciscloud.api.instance import InstanceApi


cciscloud.flaskapi.add_resource(InstanceApi, '/api/v1/instance/<string:identifier>')


if __name__ == '__main__':
    cciscloud.flaskapp.run(debug=True)
