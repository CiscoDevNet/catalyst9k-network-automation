# Catalyst 9000 Series Smart Licensing Ansible playbook

An Ansible playbook to configure and verify smart licensing on Catalyst 9000 switches

Playbooks have been tested with Ansible 2.6.4 on a Catalyst 9300 and Catalyst 9500 running IOS XE 16.09.01 

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
c2k

[c9k]
17x.2x.2xx.31
17x.2x.2xx.32
[c2k]
17x.2x.2xx.51
~~~~

# Running a Playbook
Assuming the above playbook is called smart_license.yaml, this task can then be run from a terminal window. By default, Ansible will use the hosts file located in /etc/ansible/hosts however a different hosts file can be specified using the -i flag at runtime or define it in the ansible.cfg file. In the below example we will use the -i option.
~~~~
cisco@U-Srv-18:~/playbooks$ ansible-playbook smart_license.yaml -u cisco -k -i advanced_inventory -v
Using /etc/ansible/ansible.cfg as config file
SSH password: 

PLAY [verify and configure smart license on Catalyst 9000 Series switches] ****************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************
ok: [17x.2x.2xx.32]

TASK [collect hardware facts] *************************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"ansible_facts": {"ansible_net_filesystems": ["flash:"], "ansible_net_gather_subset": ["hardware", "default"], "ansible_net_hostname": "9200-L", "ansible_net_image": "flash:packages.conf", "ansible_net_memfree_mb": 394108, "ansible_net_memtotal_mb": 518814, "ansible_net_model": "C9200L-48P-4X", "ansible_net_serialnum": "JPG221300L8", "ansible_net_stacked_models": ["C9200L-48P-4X", "C9200L-24P-4X"], "ansible_net_stacked_serialnums": ["JPG221300L8", "JPG221300AH"], "ansible_net_version": "16.09.01prd6"}, "changed": false}

TASK [set_fact] ***************************************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"ansible_facts": {"sw_version": [["16", "09"]]}, "changed": false}

TASK [fail] *******************************************************************************************************************************************************************************************
skipping: [17x.2x.2xx.32] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [Test reachability to CSSM server] ***************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"changed": false, "commands": ["ping cisco.com repeat 2"], "packet_loss": "0%", "packets_rx": 2, "packets_tx": 2, "rtt": {"avg": 44, "max": 44, "min": 44}}

TASK [run show license summary] ***********************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"changed": false, "stdout": ["Smart Licensing is ENABLED\n\nRegistration:\n  Status: UNREGISTERED\n  Export-Controlled Functionality: Not Allowed\n\nLicense Authorization: \n  Status: EVAL MODE\n  Evaluation Period Remaining: 71 days, 22 hours, 1 minutes, 59 seconds\n\nLicense Usage:\n  License                 Entitlement tag               Count Status\n  -----------------------------------------------------------------------------\n                          (C9200L-NW-E-48)                  1 EVAL MODE\n                          (C9200L-NW-E-24)                  1 EVAL MODE"], "stdout_lines": [["Smart Licensing is ENABLED", "", "Registration:", "  Status: UNREGISTERED", "  Export-Controlled Functionality: Not Allowed", "", "License Authorization: ", "  Status: EVAL MODE", "  Evaluation Period Remaining: 71 days, 22 hours, 1 minutes, 59 seconds", "", "License Usage:", "  License                 Entitlement tag               Count Status", "  -----------------------------------------------------------------------------", "                          (C9200L-NW-E-48)                  1 EVAL MODE", "                          (C9200L-NW-E-24)                  1 EVAL MODE"]]}

TASK [verify smart license status] ********************************************************************************************************************************************************************
changed: [17x.2x.2xx.32] => {"changed": true, "cmd": ["python", "verify_sl.py", "--out", "[Smart Licensing is ENABLED\\n\\nRegistration:\\n  Status: UNREGISTERED\\n  Export-Controlled\\\n    \\ Functionality: Not Allowed\\n\\nLicense Authorization: \\n  Status: EVAL MODE\\n\\\n    \\  Evaluation Period Remaining: 71 days, 22 hours, 1 minutes, 59 seconds\\n\\nLicense\\\n    \\ Usage:\\n  License                 Entitlement tag               Count Status\\n\\\n    \\  -----------------------------------------------------------------------------\\n\\\n    \\                          (C9200L-NW-E-48)                  1 EVAL MODE\\n   \\\n    \\                       (C9200L-NW-E-24)                  1 EVAL MODE]"], "delta": "0:00:00.030459", "end": "2018-09-12 09:25:46.508789", "rc": 0, "start": "2018-09-12 09:25:46.478330", "stderr": "", "stderr_lines": [], "stdout": "False", "stdout_lines": ["False"]}

TASK [fail] *******************************************************************************************************************************************************************************************
skipping: [17x.2x.2xx.32] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [set_fact] ***************************************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"ansible_facts": {"token": "ZDg1mDczODMtOGEwMS00YWNbLWI4OGEtNzI3NGNiMTA2YzFhLTE1MzZyOTM2%0AMjA3NjF8dzdIaHd3WTdKN3NDSis1ci9mWGoyVHJxZElZNVhCSQNKSEg3dHVv%0ASzMxND0%3D%0A"}, "changed": false}

TASK [configure smart token] **************************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"changed": false, "stdout": ["Registration process is in progress. Use the 'show license status' command to check the progress and result"], "stdout_lines": [["Registration process is in progress. Use the 'show license status' command to check the progress and result"]]}

TASK [pause] ******************************************************************************************************************************************************************************************
Pausing for 45 seconds
(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
ok: [17x.2x.2xx.32] => {"changed": false, "delta": 45, "echo": true, "rc": 0, "start": "2018-09-12 09:25:47.851194", "stderr": "", "stdout": "Paused for 45.0 seconds", "stop": "2018-09-12 09:26:32.851498", "user_input": ""}

TASK [run show license summary] ***********************************************************************************************************************************************************************
ok: [17x.2x.2xx.32] => {"changed": false, "stdout": ["Smart Licensing is ENABLED\n\nRegistration:\n  Status: REGISTERED\n  Smart Account: BU Production Test\n  Virtual Account: DNAC-Licensing\n  Export-Controlled Functionality: Allowed\n  Last Renewal Attempt: None\n  Next Renewal Attempt: Mar 11 16:41:39 2019 UTC\n\nLicense Authorization: \n  Status: AUTHORIZED\n  Last Communication Attempt: SUCCEEDED\n  Next Communication Attempt: Oct 12 16:41:43 2018 UTC\n\nLicense Usage:\n  License                 Entitlement tag               Count Status\n  -----------------------------------------------------------------------------\n  C9200L Network Essen... (C9200L-NW-E-48)                  1 AUTHORIZED\n  C9200L Network Essen... (C9200L-NW-E-24)                  1 AUTHORIZED"], "stdout_lines": [["Smart Licensing is ENABLED", "", "Registration:", "  Status: REGISTERED", "  Smart Account: BU Production Test", "  Virtual Account: DNAC-Licensing", "  Export-Controlled Functionality: Allowed", "  Last Renewal Attempt: None", "  Next Renewal Attempt: Mar 11 16:41:39 2019 UTC", "", "License Authorization: ", "  Status: AUTHORIZED", "  Last Communication Attempt: SUCCEEDED", "  Next Communication Attempt: Oct 12 16:41:43 2018 UTC", "", "License Usage:", "  License                 Entitlement tag               Count Status", "  -----------------------------------------------------------------------------", "  C9200L Network Essen... (C9200L-NW-E-48)                  1 AUTHORIZED", "  C9200L Network Essen... (C9200L-NW-E-24)                  1 AUTHORIZED"]]}

TASK [verify smart license status after configuration] ************************************************************************************************************************************************
changed: [17x.2x.2xx.32] => {"changed": true, "cmd": ["python", "verify_sl.py", "--out", "[Smart Licensing is ENABLED\\n\\nRegistration:\\n  Status: REGISTERED\\n  Smart Account:\\\n    \\ BU Production Test\\n  Virtual Account: DNAC-Licensing\\n  Export-Controlled Functionality:\\\n    \\ Allowed\\n  Last Renewal Attempt: None\\n  Next Renewal Attempt: Mar 11 16:41:39\\\n    \\ 2019 UTC\\n\\nLicense Authorization: \\n  Status: AUTHORIZED\\n  Last Communication\\\n    \\ Attempt: SUCCEEDED\\n  Next Communication Attempt: Oct 12 16:41:43 2018 UTC\\n\\\n    \\nLicense Usage:\\n  License                 Entitlement tag               Count\\\n    \\ Status\\n  -----------------------------------------------------------------------------\\n\\\n    \\  C9200L Network Essen... (C9200L-NW-E-48)                  1 AUTHORIZED\\n  C9200L\\\n    \\ Network Essen... (C9200L-NW-E-24)                  1 AUTHORIZED]"], "delta": "0:00:00.031347", "end": "2018-09-12 09:26:34.786718", "rc": 0, "start": "2018-09-12 09:26:34.755371", "stderr": "", "stderr_lines": [], "stdout": "True", "stdout_lines": ["True"]}

TASK [fail] *******************************************************************************************************************************************************************************************
skipping: [17x.2x.2xx.32] => {"changed": false, "skip_reason": "Conditional result was False"}

PLAY RECAP ********************************************************************************************************************************************************************************************
17x.2x.2xx.32              : ok=11   changed=2    unreachable=0    failed=0   
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
