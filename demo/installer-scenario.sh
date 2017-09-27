#/bin/bash
set -xe
cd `dirname $0`

function package-install () {
    sudo yum -y install epel-release
    sudo yum -y install collectd collectd-write_redis
    sudo yum -y install gcc gcc-c++ numpy python-devel scipy
    sudo pip install -U scikit-learn
}


LIBRARY_DIR="/opt/dma/lib"
DUMPFILE_DIR="/opt/dma/var/sklearn-dump"

COLLECTD_DIR="/etc"
COLLECTD_PLUGIN_DIR="/etc/collectd.d"
REDIS_DIR="/etc"

if [ -z "$1" ]; then
    echo "Usage: ./installer-scenario.sh <scenario-directory-name>"
    exit 1
fi
SCENARIO_DIR=$1

package-install

for i in ${LIBRARY_DIR} ${DUMPFILE_DIR}
do
    [ ! -d $i ] && sudo mkdir -p $i
done
sudo chmod 777 ${DUMPFILE_DIR}

[ -f ${COLLECTD_PLUGIN_DIR}/thresholds.conf ] && sudo mv ${COLLECTD_PLUGIN_DIR}/thresholds.conf ${COLLECTD__PLUGIN_DIR}/thresholds.conf.org
sudo cp collectd.conf ${COLLECTD_DIR}
sudo cp redis.conf ${REDIS_DIR}

sudo cp ${SCENARIO_DIR}/analysis/analysis.py ${SCENARIO_DIR}/write_python/write_congress.py ${LIBRARY_DIR}
sudo cp ${SCENARIO_DIR}/dma.conf ${COLLECTD_PLUGIN_DIR}

# is it better process restart function?
SERVICES="redis collectd"
for i in ${SERVICES}
do
    sudo systemctl enable $i
    sudo systemctl restart $i
done


echo "DMA install done!"
