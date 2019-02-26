# Configuration/Enabling BGP for VRF
Python scripts for VRF/BGP Configuration on IOS-XE devices

# define_vrf_enable_bgp.py
Script pushes the vrf and vpnv4  related config to the device.

# Usage
“python3 define_vrf_enable_bgp.py --host <ip_address> -u <username> -p <password> --vrf_name <vrf_name> --rd_val <rd_value> --rt_exp <rt_export_value> --rt_imp <rt_import_value> --int_name <interface_name> --int_num <interface_number>  --ip_add <IP_address> --sub_mask <subnet_mask> --local_as <Local_BGP_AS> --red_met <redistributed_metric> --vpn_nei <VPN_Neighbor_add> --remote_as <remote_AS_number> --source_lo_num <source_loopback_number>”

* ip_address = The Mgmt IP of the Catalyst 9000 switch 
* Username = User Login for the switch
* Password = User Password for the switch
* vrf_name = vrf name that has to be defined
* rd_value = rd value for the vrf (Eg: 1:1)
* rt_exp = rt import value for the vrf (Eg: 1:1)
* rt_imp = rt export value for the vrf (Eg: 1:1)
* int_name = interface where the vrf has to be enabled (Eg: TenGigabitEthernet,GigabitEthernet)
* int_num = interface number (Eg: 1/1/1, 2/1/1)
* ip_add =IP address of the vrf interface (Eg: 172.168.1.1)
* sub_mask = Subnet mask for above IP address ( Eg: 255.255.255.0)
* local_as = BGP Local AS number
* red_met = metric for connected redistributed routes
* vpn_nei = vpn neighbor IP address
* remote_as = remote as for the vpnv4 session
* source_lo_num = local source loopback number for BGP.

# Sample Run
➜ python3 define_vrf_enable_bgp.py --host 172.26.193.173 -u cisco -p cisco --vrf_name test6 --rd_val 6:6 --rt_exp 6:6 --rt_imp 6:6 --int_name TenGigabitEthernet --int_num 1/1/5  --ip_add 11.11.11.1 --sub_mask 255.255.255.0 --local_as 100 --red_met 10 --vpn_nei 172.168.1.80 --remote_as 100 --source_lo_num 0

vrf has been configured
Interface has been configured
BGP vrf has been configured
BGP has been configured
