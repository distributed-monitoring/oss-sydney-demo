#!/home/ubuntu/wk_takahashi/dma_venv/bin/python

# Copyright 2017 NEC Corporation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import datetime
import sys
import os
import logging
import keystoneclient.session
import keystoneclient.auth.identity
from congressclient.v1 import client


def write_log():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile = script_dir + '/log_notify.log'
    logf = open(logfile, 'a')
    logf.write(str(datetime.datetime.today()) + '\n')
    logf.write(sys.stdin.read())
    logf.write('\n==================================\n')
    logf.close


def write_rest():
    PASSWORD = 'pass'
    AUTH_URL = 'http://10.50.2.123:5000/v2.0'
    USERNAME = 'admin'
    TENANT_NAME = 'admin'

    auth = keystoneclient.auth.identity.v2.Password(
        auth_url=AUTH_URL, username=USERNAME,
        password=PASSWORD, tenant_name=TENANT_NAME)
    session = keystoneclient.session.Session(auth=auth)
    congress = client.Client(session=session,
                             auth=None,
                             interface='publicURL',
                             service_type='policy',
                             region_name='RegionOne')

    script_dir = os.path.dirname(os.path.realpath(__file__))
    logfile = script_dir + '/log_os_connect.log'
    logf = open(logfile, 'a')
    logf.write(str(datetime.datetime.today()) + '\n')
    logf.write(str(congress.list_datasources()) + '\n')
    logf.write(str(datetime.datetime.today()) + '\n')
    logf.write('\n==================================\n')
    logf.close


write_log()
# write_rest()

print 'OK'
