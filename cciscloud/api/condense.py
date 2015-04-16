from cciscloud.api import CCISCloudApi
from cciscloud.tasks.condense import Condenser
from flask.ext.restful import reqparse, Resource


class CondenseApi(CCISCloudApi):
    def post(self):
        ALLOWED_INSTANCE_TYPES = ('t2.micro',)
        #TODO: Get creator from logged in user.
        CREATOR = 'hyfi'
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', type=str, required=True)
        parser.add_argument('instance_type', choices=ALLOWED_INSTANCE_TYPES, type=str, required=True)
        parser.add_argument('description', default="Created by %s" % CREATOR, required=False)
        args = parser.parse_args()

        condenser = Condenser()
        condenser.condense(args['hostname'], CREATOR, args['description'])
        return {'status': 'success'}


