# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import collectd
import socket

import keystoneclient.session
import keystoneclient.auth.identity
from congressclient.v1 import client


class OSCliCongress:

    def __init__(self):
        self.hostname = socket.gethostname()
        self.congress = None

    def configure(self, conf):
        for node in conf.children:
            if node.key == "Username":
                username = node.values[0]
            elif node.key == "Password":
                password = node.values[0]
            elif node.key == "TenantName":
                tenant = node.values[0]
            elif node.key == "AuthURL":
                auth_url = node.values[0]
        auth = keystoneclient.auth.identity.v2.Password(
            auth_url=auth_url, username=username,
            password=password, tenant_name=tenant)
        session = keystoneclient.session.Session(auth=auth)
        self.congress = client.Client(session=session,
                                      auth=None,
                                      interface='publicURL',
                                      service_type='policy',
                                      region_name='regionOne')

    def notify(self, vl, data=None):
        if vl.severity < 4:
            data = [{"id": "1234abc", "time": vl.time, "type": vl.type,
                     "details": {"hostname": self.hostname,
                                 "status": "down_predict",
                                 "monitor": vl.plugin,
                                 "monitor_event_id": "9876xyz"}}]

            self.congress.update_datasource_rows('doctor', 'events', data)

cli = OSCliCongress()

collectd.register_config(cli.configure)
collectd.register_notification(cli.notify)
