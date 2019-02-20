# NetFlow Configuration for ETA
Python scripts for Netflow Configuration to support ETA on Catalyst 9000 switches

### ETA-Netflow.py
Script push the Netflow configuration for ETA to Catalyst 9000 Switch.

### Usage
'''
python ETA-Netflow.py --host <ip_address> -u <username> -p <password> --recordname <NetFlow_Record> --exportername <Netflow_Exporter> --exporterip <NetFlow_Exporter_IP> --exporterudpport <Exporter_UDP_Port> --monitorname <NetFlow_Monitor>
'''

<ip_addres>: The IP address of the Catalyst 9000 switch
<username> : Username for switch login (default = cisco)
<passowrd> : Password for switch logoin (default = cisco)
<NetFlow_Record> : The name of the Netflow Record (default = fnf-eta-rec)
<NetFlow_Exporter> : The name of the Netflow Exporter (default = fnf-eta-exp)
<NetFlow_Exporter_IP> : The IP address of the NetFlow collector
<Exporter_UDP_Port> : The UDP port number of the NetFlow collector (default = 2055)
<NetFlow_Monitor> : The name of the NetFlow monitor (default = fnf-eta-mon)


### Sameple Run:
cisco@U-Srv-18:~/klei$ python ETA-Netflow.py --host 172.26.202.89 --exporterip 172.26.202.123
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:856e5445-2d80-4031-92db-a7bf58705591" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <device-hardware-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper">
      <device-hardware>
        <device-system-data>
          <boot-time>2019-01-02T05:01:37+00:00</boot-time>
          <software-version>Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.9.1, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2018 by Cisco Systems, Inc.
Compiled Tue 17-Jul-18 17:00 by mcpre</software-version>
        </device-system-data>
      </device-hardware>
    </device-hardware-data>
  </data>
</rpc-reply>

Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT9K_IOSXE), Version 16.9.1, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2018 by Cisco Systems, Inc.
Compiled Tue 17-Jul-18 17:00 by mcpre
Switch Image meets the required criteria. proceeding with the configuration
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:736804e8-a910-4ea0-a9c2-3b048653b32d" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>

Configured
cisco@U-Srv-18:~/klei$
