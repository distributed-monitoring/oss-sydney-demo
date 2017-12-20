About
============

This repository contains several demo code used at OpenStack Summit Sydney, 2017, 
the lightning talk, `"DMA(Distributed Monitoring and Analysis): Monitoring Practice and Lifecycle Management for Telecom" <https://www.openstack.org/videos/sydney-2017/dmadistributed-monitoring-and-analysis-monitoring-practice-and-lifecycle-management-for-telecom>`_.

This demo code consists following parts:

Demo scenarios:

* memory-linearreg/ - detect (possible) memory leak by linear model
* memory-svm/ - detect memory leak by support vector machine (SVM)
* all_data_analytics.ipynb - detect cpu abnormal behavior by K-means

Functions:

* transmitter/ - transmit the notification from above to congress/nova

See `"Distributed Monitoring wiki page" <https://wiki.openstack.org/wiki/Distributed_Monitoring>`_ for its detail, including its architecture.

Requirements
============

This demo code requires following software:

* OpenStack (Newton or later)
  - Congress (for `transmitter/write_congress.py`)
* Collectd (>= version 5.6.x, in compute node)
* Redis (in compute node, with collectd)
* scikit-learn

Demo Install
============

(Some scenarios have indivisual README in the scenario directory. 
In that case, refer to the indivisual README first.)

::

    $ ./installer-scenario.sh <scenario-directory-name>

