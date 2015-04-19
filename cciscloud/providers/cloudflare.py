from pyflare import PyflareClient
from cciscloud import config


class CloudflareProvider():
    def __init__(self, email=config.CLOUDFLARE_EMAIL, api_key=config.CLOUDFLARE_KEY, zone='ccis.io'):
        self.zone = zone
        self.client = PyflareClient(email, api_key)

    def add_cname(self, hostname, target):
        return self.client.rec_new(self.zone, 'CNAME', hostname, target)
