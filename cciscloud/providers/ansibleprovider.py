import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
from cciscloud import config


class AnsibleProvider():
    def __init__(self, hosts, playbook):
        """
        :type hosts: list
        :type playbook: str
        """
        self.stats = callbacks.AggregateStats()
        self.playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        self.runner_cb = callbacks.PlaybookRunnerCallbacks(self.stats, verbose=utils.VERBOSITY)
        self.hosts = hosts
        self.inventory = ansible.inventory.Inventory(hosts)
        self.playbook = ansible.playbook.PlayBook(
            inventory=self.inventory,
            playbook="ansible/%s.yaml" % playbook,
            private_key_file=config.PRIVATE_KEY,
            remote_user='ec2-user',
            stats=self.stats,
            callbacks=self.playbook_cb,
            runner_callbacks=self.runner_cb
        )

    def run(self):
        return self.playbook.run()
