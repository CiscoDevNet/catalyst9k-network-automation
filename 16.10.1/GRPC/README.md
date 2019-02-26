# Streaming telemetry sessions using GRPC Dial-Out
Automation of streaming telemetry grpc (dial-out) based subscriptions on the Catalyst 9K.

### grpc-dialout.py
This python script automates streaming telemetry grpc (dial-out) based subscription on the Catalyst 9K.
It uses Jinja Templates for dynamic redering of XML payloads to netconf requests. The XML payload is kept independently inside /templates directory. 


### Usage
'''
python grpc_dialout.py --host <host_ip> -u <username> -p <password> --subscription_id <sub_id> --trigger_type <trigger_type> --period <centiseconds> --dst_ipaddr <dst_ip> --dst_port <dst_port> --xpath <xpath> 
'''

<host_ip> :	The IP address of the Catalyst 9000 switch
<username>:	Username for switch login (default = cisco)
<passowrd>:	Password for switch logoin (default = cisco)
<sub_id>  :	Subscirption ID (numeric) for the telemetry session 
<trigger_type>: Type on telemtry trigger - either 'onchange' or 'periodic' 
<period>  :	Time period in centiseconds for trigger type 'periodic' 
<dst_ip>  :	IP address for telemetry collector 
<dst_port>:	Port for telemetry colleector 
<xpath>   :	XPATH for the switch resource for the telemetry subscription
<src_ip>  :	Switch source IP address for the telemetry subscription - optional
<src_port>:	Switch source VRF for the telemetry subscription - optional


### Sample Run:

XXXXXXXXXXX$ python grpc_dialout.py -h
usage: grpc_dialout.py [-h] --host HOST [-u USERNAME] [-p PASSWORD]
                       [--port PORT] --subscription_id SUBSCRIPTION_ID
                       --trigger_type TRIGGER_TYPE [--period PERIOD]
                       --dst_ipaddr DST_IPADDR --dst_port DST_PORT --xpath
                       XPATH [--src_ipaddr SRC_IPADDR] [--src_vrf SRC_VRF]

Select options.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           The device IP or DN
  -u USERNAME, --username USERNAME
                        Go on, guess!
  -p PASSWORD, --password PASSWORD
                        Yep, this one too! ;-)
  --port PORT           Specify this if you want a non-default port
  --subscription_id SUBSCRIPTION_ID
                        Specify the id for gRPC subscription
  --trigger_type TRIGGER_TYPE
                        Specify the trigger type for gRPC subscription - must
                        be either 'onchange' or 'periodic'
  --period PERIOD       Specify the period for gRPC subscription - must for
                        trigger type 'periodic'
  --dst_ipaddr DST_IPADDR
                        Specify the destinaton address for gRPC subscription
  --dst_port DST_PORT   Specify the destination port for gRPC subscription
  --xpath XPATH         Specify the XPATH for gRPC subscription
  --src_ipaddr SRC_IPADDR
                        Optional,Specify the switch source address for gRPC
                        subscription
  --src_vrf SRC_VRF     Optional, Specify the switch source VRF for gRPC
                        subscription


python grpc_dialout.py --host x.x.x.x -u xxxx -p xxxx --subscription_id 700 --trigger_type onchange  --dst_ipaddr x.x.x.x --dst_port xxxx --xpath /cdp-ios-xe-oper:cdp-neighbor-details/cdp-neighbor-detail --src_ipaddr x.x.x.x --src_vrf Mgmt-vrf
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:25beb81c-ce7c-4024-ab95-b6ab6e586ba0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>

HURRAAY!! Telemetry subscription has beeen configured.


python grpc_dialout.py --host x.x.x.x -u xxxx -p xxxx --subscription_id 800 --trigger_type periodic --period 6000 --dst_ipaddr x.x.x.x --dst_port xxx --xpath /memory-ios-xe-oper:memory-statistics/memory-statistic 
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:54aaef94-e7fd-4f2e-a5cb-8addf35077db" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>

HURRAAY!! Telemetry subscription has beeen configured.
