import threading
from cciscloud.models.cloudinit import generate_user_data
from cciscloud.models.instance import Instance
from cciscloud.providers.ec2 import EC2Provider
from cciscloud.tasks.DNSTask import DNSTask
from cciscloud.tasks.ansiblerun import AnsibleTask


class Condenser():
    """ Condense an instance in Amazon VPC """

    def __init__(self):
        self.provider = EC2Provider()

    def condense(self, hostname, creator, description, ansibleTask):
        """
        :param hostname:
        :param creator:
        :param description:
        :param ansibleTask:
        :rtype: boto.ec2.instance.Instance
        """
        instance = self.provider.condense(hostname,
                                          creator,
                                          description,
                                          ansibleTask,
                                          generate_user_data("%s.%s.ccis.io" % (hostname, creator)))
        self.start_async_tasks(instance, ansibleTask)
        return instance

    def start_async_tasks(self, instance, ansibleTask):
        """
        Start the asynchronous tasks in their own thread.
        :param instance: boto.ec2.instance.Instance
        """
        self.thread = threading.Thread(target=self.async_tasks, args=(instance, ansibleTask,))
        self.thread.daemon = True
        self.thread.start()


    def async_tasks(self, instance, ansibleTask):
        DNSTask(Instance.from_instance_id(instance.id)).run()
        AnsibleTask(instance, ansibleTask).run()
