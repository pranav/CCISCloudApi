from flask import request
from cciscloud.api import CCISCloudApi
from cciscloud.models.instance import Instance
from cciscloud.tasks.condense import Condenser
from flask.ext.restful import reqparse, Resource


class InstanceApi(CCISCloudApi):

    ALLOWED_INSTANCE_TYPES = ('t2.micro',)

    def get(self, identifier):
        """
        :param identifier: String that can be some unique identifier like hostname or instance_id
        """
        if identifier == u'all':
            instances = [inst.to_dict() for inst in Instance.get_user_instances(request.authorization.username)]
            return instances
        else:
            #TODO: Separate cost into different api, this makes it too slow
            return Instance.find_by_identifier(identifier).to_dict()

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

        return {'status': 'success'}

    def delete(self, identifier):
        Instance.terminate_instance(identifier)
        return {'status': 'success'}

    def post(self, identifier):
        creator = request.authorization.username

        parser = reqparse.RequestParser()
        parser.add_argument('hostname', type=str, required=True)
        parser.add_argument('instance_type', choices=self.ALLOWED_INSTANCE_TYPES, type=str, required=True)
        parser.add_argument('description', default="Created by %s" % creator, required=False)
        parser.add_argument('ansibleTask', default="base", required=False)
        args = parser.parse_args()
        condenser = Condenser()
        instance = condenser.condense(args['hostname'], creator, args['description'], args['ansibleTask'])
        return {'status': 'success', 'instance_id': instance.id }
