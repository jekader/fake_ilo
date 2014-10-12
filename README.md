fake_ilo
========

iLO emulator which can power cycle libvirt VMs. It was written by me to perform tests of oVirt/RHEV Power Management features by installing hosts as libvirt VMs and querying/fencing them using this script for demo purposes.

The script is installed on a libvirt host, inside which an oVirt cluster is deployed as VMs. I
See the below picture as an example:

```
----------------------------------------------------------
| --------------  ---------------  ----------------      |
| |oVirt-host1 |  | obirt-host2 |  | ovirt-engine | -    |
| --------------  ---------------  ----------------  |   |
|       |             |              |               v   |
|       #### KVM host with libvirt ####  <----  fake_ilo |
----------------------------------------------------------
```

You do not install the script directly on oVirt nodes you are testing - it needs to control the "hardware" of this nodes, which in this case is libvirt+KVM.

DISCLAIMER:
-----------
This script was made for testing purposes only with no security in mind. The quality of code may be dangerous for mental health of the observer. Use at your own risk.

INSTALL:
--------

a) as .deb file:

1. install dependencies:
 `$ sudo apt-get install git devscripts debhelper make`

2. fetch the source and build the package:

 `$ git clone https://github.com/jekader/fake_ilo.git`
 `$ tar -cjf fake-ilo_0.0.1.orig.tar.bz2 fake_ilo/`
 `$ cd fake_ilo`
 `$ debuild -us -uc`

3. install the resulting .deb
 `$ sudo dpkg -i ../fake-ilo_0.0.1-1_amd64.deb`

b) manually:

1. install dependencies:
 `$ sudo apt-get install git make`

2. fetch the source and build the package:

 `$ git clone https://github.com/jekader/fake_ilo.git`
 `$ cd fake_ilo`
 `$ make`
 `$ sudo make install`

ENABLE:
-------

register the init script (Debian):

 `update-rc.d fake_ilo enable`


CUSTOM CERTIFICATE:
-------------------

The install script creates a default certificate which should be enough for testing. To replace it, follwo the steps:

1. go into the config directory and generate a self-signed certificate by running this command. Data provided in the requested fields is not important: oVirt does not verify certificates:

 `# cd /etc/fake_ilo/`

 `# openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt -nodes -days 9999`
 
USAGE:
------
 
 The script starts listening on port 1234 and uses the username sent from the oVirt fencing agent as the name of the VM to query/fence. The password is not important. When a username is not equal to any VM name on the machine, "NaN" is returned, which should produce an error on oVirt side. Logs are written to /var/log/fake_ilo.log
 
 Most of the settings are hardcoded, but the code is pretty simple so they can be changed as needed.
 
TROUBLESHOOTING:
----------------

To test the script, install the fence agent (should be installed on oVirt nodes by default):

 `# yum install fence-agents`
 
On the libvirt host run fake_ilo in foreground:

 `# /usr/local/bin/ilo.py`
 
Test the fence agent manually:

 `# fence_ilo -a 192.168.0.123 -u 1234 -l test -p test -o status`
 
Observe the errors displayed by the script
