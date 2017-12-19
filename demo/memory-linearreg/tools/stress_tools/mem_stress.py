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

import sys
import subprocess
import time
import math

args = sys.argv

if len(args) != 5:
    print 'Usage: Bytes Counts Interval_sec Stress_keep_time'
    sys.exit(1)

[_, membytes, counts_str, interval_str, keeptime_str] = args

counts = int(counts_str)
interval = float(interval_str)
keeptime = int(keeptime_str)

for timestep in [interval*t+keeptime for t in range(counts-1, -1, -1)]:
    cmd = 'stress -m 1 --vm-bytes '
    cmd += membytes
    cmd += ' --vm-keep -t '
    cmd += str(math.ceil(timestep))
    cmd += ' &'
    subprocess.call(cmd, shell=True)
    time.sleep(interval)

time.sleep(1)
print 'Stress keep...'
time.sleep(keeptime)

print 'OK'
