from cciscloud.tasks.condense import Condenser
from flask.ext.restful import reqparse, Resource


class CondenseApi(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', type=str, required=True)
        args = parser.parse_args()
        condenser = Condenser()
        #TODO: Get creator from logged in user.
        condenser.condense(args['hostname'], 'hyfi')
        return {'status': 'success'}


