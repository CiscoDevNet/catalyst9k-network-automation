###StackWise Virtual for Catalyst 9K
Python scripts for Stackwise Virtual Configuration on Catalyst 9000 switche.

##svl.yaml
Script pushes the Stackwise Virtual configuration to Catalyst 9000 Switches.

## Advaned_invertory
Need to assigne the switch IP addresses at the advanced inventory file.

###Usage
'''  Ansible-playbook svl.yaml -vvv -u xxxxx -k -i advanced_inventory -v --extra-vars="domain=10 intf1=2/0/1 intf2=2/0/2 dadintf=2/0/3"'''

The assigned interfaces can only be 10G interfaces for SVL and DAD ports. In the later releases we will add to chose any type of interface.
Device IP addresses has to entered in the advanced inventory file and Username, Password ,Interfaces and Domain needs to be defined by the user.


2019-01-02T05:01:37+00:00 Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.9.1, RELEASE SOFTWARE (fc2) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2018 by Cisco Systems, Inc. Compiled Tue 17-Jul-18 17:00 by mcpre
Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.9.1, RELEASE SOFTWARE (fc2) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2018 by Cisco Systems, Inc. Compiled Tue 17-Jul-18 17:00 by mcpre Switch Image meets the required criteria. proceeding with the configuration

