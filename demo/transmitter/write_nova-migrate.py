import collectd
import socket
import sys
from novaclient import client


class OSCliNova:

    def __init__(self):
        self.hostname = socket.getfqdn()
        self.novaclient = None

    def configure(self, conf):
        for node in conf.children:
            if node.key == "Username":
                username = node.values[0]
            elif node.key == "Password":
                password = node.values[0]
            elif node.key == "TenantName":
                tenant_name = node.values[0]
            elif node.key == "AuthURL":
                auth_url = node.values[0]
        self.novaclient = client.Client(version='1.1',
                                        username=username,
                                        password=password,
                                        project_id=tenant_name,
                                        auth_url=auth_url,
                                        connection_pool=True)
        # print >> sys.stderr, (username, password, tenant_name, auth_url)

    def notify(self, vl, data=None):
        if vl.severity < 4:
            hypervisors = self.novaclient.hypervisors.search(
                              self.hostname, servers=True)
            for hyper in hypervisors:
                if hasattr(hyper, 'servers'):
                    for server in hyper.servers:
                        self.novaclient.servers.migrate(server['uuid'])


cli = OSCliNova()

collectd.register_config(cli.configure)
collectd.register_notification(cli.notify)
