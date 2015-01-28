from cciscloud.models.instance import Instance
from cciscloud.tasks.condense import Condenser
from flask.ext.restful import reqparse, Resource


class InstanceApi(Resource):
    def get(self, identifier):
        """
        :param identifier: String that can be some unique identifier like hostname or instance_id
        """
        if identifier == u'all':
            #TODO: Get username from request.
            instances = [inst.__dict__ for inst in Instance.get_user_instances('hyfi')]
            return instances
        else:
            return Instance.find_by_identifier(identifier).__dict__

    def put(self, identifier):
        """

        :param identifier: str instance_id
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('action', choices=('start', 'stop', 'reboot'), type=str, required=True)
        args = parser.parse_args()

        if args['action'] == 'start':
            Instance.start_instance(identifier)
        elif args['action'] == 'stop':
            Instance.stop_instance(identifier)
        elif args['action'] == 'reboot':
            Instance.reboot_instance(identifier)

        return { 'status': 'success' }

    def delete(self, identifier):
        Instance.terminate_instance(identifier)
        return {'status': 'success'}

    def post(self, identifier):
        ALLOWED_INSTANCE_TYPES = ('t2.micro',)
        #TODO: Get creator from logged in user.
        CREATOR = 'hyfi'
        parser = reqparse.RequestParser()
        parser.add_argument('hostname', type=str, required=True)
        parser.add_argument('instance_type', choices=ALLOWED_INSTANCE_TYPES, type=str, required=True)
        parser.add_argument('description', default="Created by %s" % CREATOR, required=False)
        parser.add_argument('puppetClass', default="ccis::role_base", required=False)
        args = parser.parse_args()
        condenser = Condenser()
        condenser.condense(args['hostname'], CREATOR, args['description'], args['puppetClass'])
        return {'status': 'success'}
