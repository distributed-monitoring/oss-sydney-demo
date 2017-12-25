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

import sys
from datetime import datetime
import time

# from sklearn import datasets
from sklearn import svm
from sklearn.preprocessing import StandardScaler
import redis
from sklearn.externals import joblib

NORMAL = 0
FAULT = 1

# Later, move to configure...
stddumpfile = '/opt/dma/var/sklearn-dump/std.cmp'
scdumpfile = '/opt/dma/var/sklearn-dump/svm.cmp'


def read_redis(stime, etime, stat):
    conn = redis.StrictRedis(host='localhost', port=6379)
    rawlist = conn.zrangebyscore('collectd/localhost/memory/memory-used',
                                 stime, etime)
    datalist = [s.split(":") for s in rawlist]
    dlist = [[float(d[1]), float(d[1])] for d in datalist]
    llist = [stat for d in datalist]
    print("DEBUG read: ", dlist)
    print("DEBUG read: ", llist)
    return (dlist, llist)


def learn(dlist, llist):
    std_scl = StandardScaler()
    std_scl.fit(dlist)
    dlist_std = std_scl.transform(dlist)
    clf = svm.SVC()
    clf.fit(dlist_std, llist)
    print("DEBUG learn: ", dlist)
    print("DEBUG learn: ", dlist_std)
    print("DEBUG learn: ", llist)
    joblib.dump(std_scl, stddumpfile, compress=True)
    joblib.dump(clf, scdumpfile, compress=True)
    return


def date2sec(datestr):
    date = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S")
    sec = int(time.mktime(date.timetuple()))
    # print sec
    return sec


argvs = sys.argv
argc = len(argvs)

# print argvs
# print argc
# print
if (argc != 5):
    print ('Usage: python learn.py '
           '<normal-start> <normal-end> <fault-start> <fault-end>')
    quit()

normalinput = read_redis(date2sec(argvs[1]), date2sec(argvs[2]), NORMAL)
faultinput = read_redis(date2sec(argvs[3]), date2sec(argvs[4]), FAULT)
learn(normalinput[0] + faultinput[0], normalinput[1] + faultinput[1])
