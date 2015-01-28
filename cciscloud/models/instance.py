import re
import json
from cciscloud.providers.ec2 import EC2Provider


class Instance():
    def __init__(self, state, dns_name, ebs_optimized, eventsSet, instance_id, image_id, instance_type,
                 public_ip_address, key_name, launch_time, private_ip_address, public_dns_name, region,
                 tags, virtualization_type, vpc_id):
        self.state = state
        self.dns_name = dns_name
        self.ebs_optimized = ebs_optimized
        self.eventsSet = eventsSet
        self.instance_id = instance_id
        self.image_id = image_id
        self.instance_type = instance_type
        self.public_ip_address = public_ip_address
        self.key_name = key_name
        self.launch_time = launch_time
        self.private_ip_address = private_ip_address
        self.public_dns_name = public_dns_name
        self.region = region
        self.tags = tags
        self.virtualization_type = virtualization_type
        self.vpc_id = vpc_id

    @staticmethod
    def get_user_instances(creator):
        ec2 = EC2Provider()
        return [Instance.from_EC2Instance(inst) for inst in ec2.get_instances_by_tag('creator', creator)]

    @staticmethod
    def find_by_identifier(identifier):
        """

        :type identifier: str
        :return: Instance
        """
        if re.match(r'i-[a-z0-9]+', identifier):
            return Instance.from_instance_id(identifier)
        else:
            return Instance.from_hostname(identifier)

    @staticmethod
    def from_hostname(hostname):
        ec2 = EC2Provider()
        return Instance.from_EC2Instance(ec2.get_instances_by_tag("hostname", hostname)[0])

    @staticmethod
    def from_EC2Instance(ec2_instance):
        """
        Construct Instance from boto Instance
        :type ec2_instance: boto.ec2.instance.Instance
        :return: Instance
        """
        return Instance(ec2_instance._state.name, ec2_instance.dns_name,
                        ec2_instance.ebs_optimized, ec2_instance.eventsSet, ec2_instance.id, ec2_instance.image_id, ec2_instance.instance_type,
                        ec2_instance.ip_address, ec2_instance.key_name, ec2_instance.launch_time,
                        ec2_instance.private_ip_address, ec2_instance.public_dns_name,
                        ec2_instance.region.name, ec2_instance.tags, ec2_instance.virtualization_type,
                        ec2_instance.vpc_id)

    @staticmethod
    def from_instance_id(instance_id):
        return Instance.from_EC2Instance(EC2Provider().get_instance_by_id(instance_id))
