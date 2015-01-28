from cciscloud.models.instance import Instance
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
        return Instance.terminate_instance(identifier)