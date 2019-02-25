###StackWise Virtual for Catalyst 9K
Python scripts for Stackwise Virtual Configuration on Catalyst 9000 switches.

##svl.yaml
Script pushes the Stackwise Virtual configuration to Catalyst 9000 Switches.

##Advaned_invertory
Need to add the SVL switch IP addresses (2 switches) in file "advanced_inventory".

##Usage
'''  ansible-playbook svl.yaml -vvv -u xxxxx -k -i advanced_inventory -v --extra-vars="domain=10 intf1=2/0/1 intf2=2/0/2 dadintf=2/0/3"'''

domain: Sets the Stackwise virtual domain in global configuration for both the SVL switches. The domain range can be any number between 1 to 255. 
intf1:  Sets Stackwise virtual Link on the defined interface as long as both the interfaces are similar on both SVL switches. SVL link number will always be set to 1.
intf2:  Sets Stackwise virtual Link on the defined interface as long as both the interfaces are similar on both SVL switches. SVL link number will always be set to 1.
dadintf:Sets Stackwise virtual Dual Active Detection Link on the defined interface as long as both the interfaces are similar on both SVL switches.
Notes:
-The assigned interfaces can only be 10G interfaces for SVL and DAD ports. In the later releases we will add to chose any type of interface.
-Device IP addresses has to entered in the advanced inventory file and Username, Password ,Interfaces and Domain needs to be defined by the user at execution time.
