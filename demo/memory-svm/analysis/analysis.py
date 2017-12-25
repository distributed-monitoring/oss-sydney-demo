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

import os.path

# from sklearn import datasets
import redis
from sklearn.externals import joblib

# Later, move to configure...
stddumpfile = '/opt/dma/var/sklearn-dump/std.cmp'
scdumpfile = '/opt/dma/var/sklearn-dump/svm.cmp'


class Analysis:
    def __init__(self):
        self.std = None
        self.clf = None

    def read_redis(self):
        conn = redis.StrictRedis(host='localhost', port=6379)
        rawlist = conn.zrange('collectd/localhost/memory/memory-used',
                              -2, -1)
        datalist = rawlist[0].split(":")
        xval = float(datalist[0])
        yval = float(datalist[1])
        # print(xval)
        # print(yval)
        return (xval, yval)

    def analysis(self, (xval, yval)):
        # [a] = clf.coef_
        # b = clf.intercept_
        # print("a:", a)
        # print("b:", b)
        # print("time:",predict_time)
        data_std = self.std.transform([[yval, yval]])
        return self.clf.predict(data_std)[0]

    def put_result(self, result):
        vl = collectd.Values(host='localhost', plugin='dma', type='gauge')
        vl.dispatch(values=[max(int(result), 0)])

    def configure(self, conf):
        if os.path.exists(stddumpfile) and os.path.exists(scdumpfile):
            self.std = joblib.load(stddumpfile)
            self.clf = joblib.load(scdumpfile)
        else:
            print "analysis: missing dumpfile"

    def read(self):
        self.put_result(self.analysis(self.read_redis()))


obj = Analysis()

if __name__ == "__main__":
    obj.configure(None)
    print obj.analysis(obj.read_redis())
else:
    import collectd

    collectd.register_config(obj.configure)
    collectd.register_read(obj.read, 1)
