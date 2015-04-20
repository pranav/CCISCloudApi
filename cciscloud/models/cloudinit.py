from jinja2 import Template


def generate_user_data(fqdn):
    cloud_template = """#cloud-config

hostname: {{ fqdn.split('.')[0] }}
fqdn: {{ fqdn }}
manage_etc_hosts: true
preserve_hostname: false
"""
    return Template(cloud_template).render(locals())
