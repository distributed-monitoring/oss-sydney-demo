Memory Leak Demo Install
========================

Notification Setting
--------------------

Create "dma.conf" to set collectd-python plugin.
You can set notifications as follows.
Set "write\_nova-migrate" by referring to the OpenStack RC file
in order to request migration to Nova directly.
Set "write\_http" as a notification destination URL.

::

    $ cp dma.conf_sample dma.conf
    $ vi dma.conf

    <Plugin python>
            ...
            <Module "write_nova-migrate">
                Username "admin"
                Password "pass"
                TenantName "admin"
                AuthURL "http://192.168.1.3:5000/v2.0"
            </Module>
    </Plugin>
    ...
    <Plugin write_http>
        <Node "mynode">
            URL "http://192.168.37.1:10021/failure"
            ...
        </Node>
    </Plugin>

Install Demo
------------

::

    $ ./installer.sh
    $ sudo yum install stress

Running the Demo
================

-  Memory bulk allocation is **not** notified.

::

    $ python tools/stress_tools/mem_stress.py 200m 16 0 5

    (Not execute migration)
    (No notification)

-  Continuous increase of memory allocate, i.e. memory leak, is
   notified.

::

    $ python tools/stress_tools/mem_stress.py 200m 16 0.7 5

    (Execute VM migration on memory leak host)
    (Notification to the set URL)

