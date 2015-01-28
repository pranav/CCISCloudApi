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
