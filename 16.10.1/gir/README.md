# Catalyst 9000 Series Smart Licensing Ansible playbook

An Ansible playbook to configure and verify GIR on Catalyst 9000 switches

Playbooks have been tested with Ansible 2.6.4 on a Catalyst 9300 and Catalyst 9500 running IOS XE 16.10.1 

# Installation

To install latest version of Ansible on servers running the most popular Linux distributions like Red Hat, CentOS, Fedora, Debian, or Ubuntu, the OS package manager can be used.

Installation via the Python package manager (pip), is available as well.

All the Cisco IOS XE modules are included in Ansible Core so no aditional effort is required to begin automating your Cisco IOS XE devices. As Ansible has an agentless architecture, once username and password are configured/provided, then the devices can be managed through Ansible. The username provided with the playbook must have the requisite role privilege to allow device configuration changes.

Fedora, CentOS, RedHat:
Installation using yum package manager:

~~~~
$sudo yum install ansible
~~~~

## Installation using pip:

~~~~
$sudo pip install ansible
~~~~

In case pip is not installed on the server yet, it can be installed using the yum package manager again:

~~~~
$ sudo yum install python-pip
~~~~

Debian, Ubuntu:
Installation using apt-get package manager:

~~~~
$ sudo apt-get install ansible
~~~~

## Installation using pip:

~~~~
$ sudo pip install ansible
~~~~
In case pip is not installed on the server yet, it can be installed using the apt-get package manager again:

~~~~
$ sudo apt-get install python-pip
~~~~

OSX:
pip is the recommended installation method on OSX.

~~~~
$ sudo pip install ansible
~~~~

In case pip is not installed on the Mac yet, it can be installed using the easy_install Python Tool:
~~~~
$ sudo easy_install pip
~~~~

# Ansible version
After installation, on any Linux distro, you can check the Ansible version installed.
~~~~
ansible 2.6.4
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/cisco/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.15rc1 (default, Apr 15 2018, 21:51:34) [GCC 7.3.0]
~~~~

# Hosts File
The host file is where the devices under management are listed. A single device can be in a single group or included in multiple groups. In the below hosts file we have a multiple groups called c9k and c2k, each of which has devices under it. The connection is set to local as we will be connecting SSH to manage the devices.
~~~~
bash-4.1$ cat advanced_inventory 
[all:vars]
ansible_connection = local
ansible_python_interpreter=python

[switches:children]
c9k

[c9k]
172.xx.x00.xxx
~~~~

# Running a Playbook
Assuming the above playbook is called smart_license.yaml, this task can then be run from a terminal window. By default, Ansible will use the hosts file located in /etc/ansible/hosts however a different hosts file can be specified using the -i flag at runtime or define it in the ansible.cfg file. In the below example we will use the -i option.
~~~~
cisco@U-Srv-18:~/gir$ ansible-playbook gir.yaml -vvv -u cisco -k -i advanced_inventory -v --extra-vars="neighbour_ip=15.15.15.2 timeout_period=20 ansible_user_pwd=cisco ansible_successor=Core1 self_ip=17x.x6.x00.xxx"
ansible-playbook 2.7.7
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/cisco/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.15rc1 (default, Nov 12 2018, 14:31:15) [GCC 7.3.0]
Using /etc/ansible/ansible.cfg as config file
SSH password: 
setting up inventory plugins
/home/cisco/minhaj_gir/advanced_inventory did not meet host_list requirements, check plugin documentation if this is unexpected
/home/cisco/minhaj_gir/advanced_inventory did not meet script requirements, check plugin documentation if this is unexpected
Parsed /home/cisco/minhaj_gir/advanced_inventory inventory source with ini plugin
Loading callback plugin default of type stdout, v2.0 from /usr/lib/python2.7/dist-packages/ansible/plugins/callback/default.pyc

PLAYBOOK: try.yaml *****************************************************************************************************************************************************************************************
1 plays in try.yaml

PLAY [Configure GIR on Catalyst 9000 Series switches] ******************************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************************************************************************
task path: /home/cisco/minhaj_gir/try.yaml:29
<172.26.200.117> ESTABLISH LOCAL CONNECTION FOR USER: cisco
<172.26.200.117> EXEC /bin/sh -c 'echo ~cisco && sleep 0'
<172.26.200.117> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109 `" && echo ansible-tmp-1556213136.4-218012872313109="` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109 `" ) && sleep 0'
Using module file /usr/lib/python2.7/dist-packages/ansible/modules/system/setup.py
<172.26.200.117> PUT /home/cisco/.ansible/tmp/ansible-local-91784g921z/tmpARX7vE TO /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109/AnsiballZ_setup.py
<172.26.200.117> EXEC /bin/sh -c 'chmod u+x /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109/ /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109/AnsiballZ_setup.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'python /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109/AnsiballZ_setup.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'rm -f -r /home/cisco/.ansible/tmp/ansible-tmp-1556213136.4-218012872313109/ > /dev/null 2>&1 && sleep 0'
ok: [172.26.200.117]
META: ran handlers

TASK [GRABBING CDP NEIGHBORS] ******************************************************************************************************************************************************************************
task path: /home/cisco/minhaj_gir/try.yaml:35
<172.26.200.117> using connection plugin network_cli (was local)
<172.26.200.117> starting connection from persistent connection plugin
<172.26.200.117> local domain socket does not exist, starting it
<172.26.200.117> control socket path is /home/cisco/.ansible/pc/fc0108a544
<172.26.200.117> <172.26.200.117> ESTABLISH PARAMIKO SSH CONNECTION FOR USER: cisco on PORT 22 TO 172.26.200.117
<172.26.200.117> <inventory_hostname> ssh connection done, setting terminal
<172.26.200.117> <inventory_hostname> loaded terminal plugin for network_os ios
<172.26.200.117> <inventory_hostname> loaded cliconf plugin for network_os ios
<172.26.200.117> <172.26.200.117> Response received, triggered 'persistent_buffer_read_timeout' timer of 0.1 seconds
<172.26.200.117> <inventory_hostname> firing event: on_open_shell()
<172.26.200.117> <172.26.200.117> Response received, triggered 'persistent_buffer_read_timeout' timer of 0.1 seconds
<172.26.200.117> <172.26.200.117> Response received, triggered 'persistent_buffer_read_timeout' timer of 0.1 seconds
<172.26.200.117> <inventory_hostname> ssh connection has completed successfully
<172.26.200.117> connection to remote device started successfully
<172.26.200.117> local domain socket listeners started successfully
<172.26.200.117> 
<172.26.200.117> local domain socket path is /home/cisco/.ansible/pc/fc0108a544
<172.26.200.117> socket_path: /home/cisco/.ansible/pc/fc0108a544
<172.26.200.117> ESTABLISH LOCAL CONNECTION FOR USER: cisco
<172.26.200.117> EXEC /bin/sh -c 'echo ~cisco && sleep 0'
<172.26.200.117> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632 `" && echo ansible-tmp-1556213138.88-54797421651632="` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632 `" ) && sleep 0'
Using module file /usr/lib/python2.7/dist-packages/ansible/modules/network/ios/ios_command.py
<172.26.200.117> PUT /home/cisco/.ansible/tmp/ansible-local-91784g921z/tmp9d8Dx2 TO /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632/AnsiballZ_ios_command.py
<172.26.200.117> EXEC /bin/sh -c 'chmod u+x /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632/ /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632/AnsiballZ_ios_command.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'python /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632/AnsiballZ_ios_command.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'rm -f -r /home/cisco/.ansible/tmp/ansible-tmp-1556213138.88-54797421651632/ > /dev/null 2>&1 && sleep 0'
ok: [172.26.200.117] => {
    "changed": false, 
    "invocation": {
        "module_args": {
            "auth_pass": null, 
            "authorize": null, 
            "commands": [
                "show cdp neighbors"
            ], 
            "host": null, 
            "interval": 1, 
            "match": "all", 
            "password": null, 
            "port": null, 
            "provider": {
                "auth_pass": null, 
                "authorize": null, 
                "host": null, 
                "password": null, 
                "port": null, 
                "ssh_keyfile": null, 
                "timeout": null, 
                "username": null
            }, 
            "retries": 10, 
            "ssh_keyfile": null, 
            "timeout": null, 
            "username": null, 
            "wait_for": null
        }
    }, 
    "stdout": [
        "Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge\n                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, \n                  D - Remote, C - CVTA, M - Two-port Mac Relay \n\nDevice ID        Local Intrfce     Holdtme    Capability  Platform  Port ID\nCore1            For 1/0/1         157             R S I  C9500-12Q For 1/0/2\n9300-Patching-144.cisco\n                 For 1/0/7         158             R S I  C9300-24U For 1/1/2\nD-Vlan200.cisco.com\n                 Gig 0/0           146              S I   WS-C3650- Gig 1/0/10\n\nTotal cdp entries displayed : 3"
    ], 
    "stdout_lines": [
        [
            "Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge", 
            "                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, ", 
            "                  D - Remote, C - CVTA, M - Two-port Mac Relay ", 
            "", 
            "Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID", 
            "Core1            For 1/0/1         157             R S I  C9500-12Q For 1/0/2", 
            "9300-Patching-144.cisco", 
            "                 For 1/0/7         158             R S I  C9300-24U For 1/1/2", 
            "D-Vlan200.cisco.com", 
            "                 Gig 0/0           146              S I   WS-C3650- Gig 1/0/10", 
            "", 
            "Total cdp entries displayed : 3"
        ]
    ]
}

TASK [collect hardware facts] ******************************************************************************************************************************************************************************
task path: /home/cisco/minhaj_gir/try.yaml:39
<17x.x6.x00.xxx> using connection plugin network_cli (was local)
<17x.x6.x00.xxx> starting connection from persistent connection plugin
<17x.x6.x00.xxx> found existing local domain socket, using it!
<17x.x6.x00.xxx> updating play_context for connection
<172.26.200.117> 
<172.26.200.117> local domain socket path is /home/cisco/.ansible/pc/fc0108a544
<172.26.200.117> socket_path: /home/cisco/.ansible/pc/fc0108a544
<172.26.200.117> ESTABLISH LOCAL CONNECTION FOR USER: cisco
<172.26.200.117> EXEC /bin/sh -c 'echo ~cisco && sleep 0'
<172.26.200.117> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911 `" && echo ansible-tmp-1556213140.16-265897654474911="` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911 `" ) && sleep 0'
Using module file /usr/lib/python2.7/dist-packages/ansible/modules/network/ios/ios_facts.py
<172.26.200.117> PUT /home/cisco/.ansible/tmp/ansible-local-91784g921z/tmp1A3RqH TO /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911/AnsiballZ_ios_facts.py
<172.26.200.117> EXEC /bin/sh -c 'chmod u+x /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911/ /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911/AnsiballZ_ios_facts.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'python /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911/AnsiballZ_ios_facts.py && sleep 0'
<172.26.200.117> EXEC /bin/sh -c 'rm -f -r /home/cisco/.ansible/tmp/ansible-tmp-1556213140.16-265897654474911/ > /dev/null 2>&1 && sleep 0'
ok: [172.26.200.117] => {
    "ansible_facts": {
        "ansible_net_filesystems": [
            "flash:"
        ], 
        "ansible_net_filesystems_info": {
            "flash:": {
                "spacefree_kb": 6942464, 
                "spacetotal_kb": 11087104
            }
        }, 
        "ansible_net_gather_subset": [
            "hardware", 
            "default"
        ], 
        "ansible_net_hostname": "Minhaj_MONEY", 
        "ansible_net_image": "flash:packages.conf", 
        "ansible_net_memfree_mb": 1093813, 
        "ansible_net_memtotal_mb": 1418150, 
        "ansible_net_model": "C9500-12Q", 
        "ansible_net_serialnum": "FCW2129A4G0", 
        "ansible_net_stacked_models": [
            "C9500-12Q"
        ], 
        "ansible_net_stacked_serialnums": [
            "FCW2129A4G0"
        ], 
        "ansible_net_version": "16.09.01"
    }, 
    "changed": false, 
    "invocation": {
        "module_args": {
            "auth_pass": null, 
            "authorize": null, 
            "gather_subset": [
                "hardware"
            ], 
            "host": null, 
            "password": null, 
            "port": null, 
            "provider": {
                "auth_pass": null, 
                "authorize": null, 
                "host": null, 
                "password": null, 
                "port": null, 
                "ssh_keyfile": null, 
                "timeout": null, 
                "username": null
            }, 
            "ssh_keyfile": null, 
            "timeout": null, 
            "username": null
        }
    }
}

TASK [verify smart license status after configuration] *****************************************************************************************************************************************************
task path: /home/cisco/minhaj_gir/try.yaml:43
<17x.x6.x00.xxx> ESTABLISH LOCAL CONNECTION FOR USER: cisco
<17x.x6.x00.xxx> EXEC /bin/sh -c 'echo ~cisco && sleep 0'
<17x.x6.x00.xxx> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630 `" && echo ansible-tmp-1556213141.97-164045074710630="` echo /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630 `" ) && sleep 0'
Using module file /usr/lib/python2.7/dist-packages/ansible/modules/commands/command.py
<17x.x6.x00.xxx> PUT /home/cisco/.ansible/tmp/ansible-local-91784g921z/tmpiomo2j TO /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630/AnsiballZ_command.py
<17x.x6.x00.xxx> EXEC /bin/sh -c 'chmod u+x /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630/ /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630/AnsiballZ_command.py && sleep 0'
<17x.x6.x00.xxx> EXEC /bin/sh -c 'python /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630/AnsiballZ_command.py && sleep 0'
<17x.x6.x00.xxx> EXEC /bin/sh -c 'rm -f -r /home/cisco/.ansible/tmp/ansible-tmp-1556213141.97-164045074710630/ > /dev/null 2>&1 && sleep 0'
minhaj_gir/try.retry

PLAY RECAP *************************************************************************************************************************************************************************************************
17x.x6.x00.xxx             : ok=3    changed=1    unreachable=0    failed=0   

~~~~

# Debugging
In case of errors, the playbook cab be run with the verbose option with -vvvv flag.

# Logging
Ansible also has built-in support for logging. The log file can be defined either in the ansible.cfg file or by defining the ANSIBLE_LOG_PATH environment variable

~~~~
$ cat ansible.cfg
[defaults] 
log_path=/var/log/ansible.log

$ export ANSIBLE_LOG_PATH=/var/log/ansible.log
~~~~
