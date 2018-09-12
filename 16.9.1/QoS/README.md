QoS Features
This is a sample Python script, that intends to configure QoS feature sets such as Class-map that matches on DSCP value, Policy-map that uses multiple class-maps and attach the policy-map to interface. 
This script also give option to set QoS SoftMax global parameter.
The script provides functions which can read the configured values or read individual class-map and policy-map names.
requirements
-- ncclient, sys, argparse,  xml.etree.ElementTree, re, logging, cmd and  xmltodict

-- IOS-XE running >/= 16.8.1 also enabled for NETCONF
running
-- Can run on-box or off-box.

