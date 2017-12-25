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

import collectd
# from sklearn import datasets
from sklearn import linear_model
import redis

datasize = 20
predict_after = 60


def read_redis():
    conn = redis.StrictRedis(host='localhost', port=6379)
    rawlist = conn.zrange('collectd/localhost/memory/memory-used',
                          -datasize, -1)
    datalist = [s.split(":") for s in rawlist]
    xlist = [[float(d[0])] for d in datalist]
    ylist = [float(d[1]) for d in datalist]
    # print(xlist)
    # print(ylist)
    return (xlist, ylist)


def analysis((xlist, ylist)):
    predict_time = xlist[-1][0] + predict_after
    clf = linear_model.LinearRegression()
    clf.fit(xlist, ylist)
    # [a] = clf.coef_
    # b = clf.intercept_
    # print("a:", a)
    # print("b:", b)
    # print("time:",predict_time)
    return clf.predict([[predict_time]])[0]


def put_result(result):
    vl = collectd.Values(host='localhost', plugin='dma', type='memory')
    vl.dispatch(values=[max(int(result), 0)])


def configure(conf):
    print 'no conf'


collectd.register_config(configure)
collectd.register_read(lambda: put_result(analysis(read_redis())), 1)
