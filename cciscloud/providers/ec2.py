import boto
from cciscloud import config


class EC2Provider():
    """ Provider for interfacing with EC2 """

    def __init__(self, aws_access_key_id=config.AWS_ACCESS_KEY,
                 aws_secret_access_key=config.AWS_SECRET_KEY):
        self.conn = boto.connect_ec2(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key)

    def condense(self, hostname, creator, ami=config.DEFAULT_AMI,
                 instance_type=config.DEFAULT_INSTANCE,
                 security_group_ids=[config.DEFAULT_SECURITY_GROUP],
                 dry_run=False):
        self.reservation = self.conn.run_instances(ami, key_name=config.ROOT_KEY,
                                                   instance_type=instance_type,
                                                   security_group_ids=security_group_ids,
                                                   subnet_id=config.PUBLIC_SUBNET_ID,
                                                   dry_run=dry_run)
        self.reservation.instances[0].add_tags({'hostname': hostname,
                                                'Name': hostname,
                                                'creator': creator})
        return self.reservation.instances[0]

    def get_instances_by_tag(self, tag_name, tag_value):
        instances = self.conn.get_only_instances(filters={("tag:%s" % tag_name): tag_value})
        return instances

    def get_instance_by_id(self, instance_id):
        return self.conn.get_only_instances(instance_ids=[instance_id])[0]

    def stop_instance(self, instance_id):
        return self.conn.stop_instances(instance_ids=[instance_id])

    def start_instance(self, instance_id):
        return self.conn.start_instances(instance_ids=[instance_id])

    def reboot_instance(self, instance_id):
        return self.conn.reboot_instances(instance_ids=[instance_id])

    def delete_instance(self, instance_id):
        return self.conn.terminate_instances(instance_ids=[instance_id])[0]
