import threading
import time
from cciscloud.models.instance import Instance
from cciscloud.providers.cloudflare import CloudflareProvider


class DNSTask():
    def __init__(self, instance):
        """
        :type instance: cciscloud.models.instance.Instance
        """
        self.instance = instance

    def run(self):
        while True:
            self.instance = Instance.from_instance_id(self.instance.instance_id)
            time.sleep(1)
            try:
                if not (self.instance.public_dns_name is None) and len(self.instance.public_dns_name) > 2:
                    CloudflareProvider().add_cname(self.instance.tags['Name']+'.'+self.instance.tags['creator'],
                                                   self.instance.public_dns_name)
                    break
            except AttributeError:
                pass
