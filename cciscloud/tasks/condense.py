from cciscloud import ANSIBLE_QUEUE
from cciscloud.providers.ec2 import EC2Provider
from cciscloud.tasks.ansiblerun import AnsibleTask


class Condenser():
    """ Condense an instance in Amazon VPC """

    def __init__(self):
        self.provider = EC2Provider()

    def condense(self, hostname, creator, description, puppetClass):
        instance = self.provider.condense(hostname, creator, description, puppetClass)
        ansibletask = AnsibleTask(instance, "base").start()
