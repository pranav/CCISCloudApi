import boto
from cciscloud.providers.ec2 import EC2Provider


class Condenser():
    """ Condense an instance in Amazon VPC """

    def __init__(self):
        self.provider = EC2Provider()

    def condense(self, hostname, creator):
        self.provider.condense(hostname, creator)
