import time
import socket
import threading
from cciscloud.models.instance import Instance
from cciscloud.providers.ansibleprovider import AnsibleProvider


class AnsibleTask():
    def __init__(self, instance, playbook):
        """
        :type ansible_provider: AnsibleProvider
        :type instance: boto.ec2.instance.Instance
        """
        self.instance_id = instance.id
        self.playbook = playbook
        self.thread = threading.Thread(target=self.task)
        self.thread.daemon = True

    def task(self):
        instance = Instance.from_instance_id(self.instance_id)
        while True:
            instance = Instance.from_instance_id(self.instance_id)
            if AnsibleTask.check_ssh_open(instance):
                break
            time.sleep(1)
        return AnsibleProvider([instance.public_ip_address], self.playbook).run()

    def start(self):
        return self.thread.start()

    @staticmethod
    def check_ssh_open(instance):
        """
        Checks if SSH is accepting connections
        :type instance: Instance
        :return: boolean
        """
        if instance.public_ip_address is None:
            return False
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((instance.public_ip_address, 22))
            sock.recv(2048)
            sock.send("SSH-2.0-billsSSH_3.6.3q3\n")
            sock.recv(2048)
            return True
        except (socket.errno, socket.error, socket.timeout) as e:
            return False
        finally:
            sock.close()
