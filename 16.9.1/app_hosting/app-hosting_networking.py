#!/usr/bin/env python3
#
# Copyright (c) 2018, Cisco and/or its affiliates
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# This script configures IP address and gateway of the applictaion which is deployed on Catalyst 9K.



import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
import re
import logging
import checkversion
from xml.etree.ElementTree import XML 



def modify_app_resources(netconf_connection, appplication_name, ip, mask, gateway):
  '''
  This procedure verifies the application name, IP address, Mask and Default gateway. 
  Return True if condition satisfied, else return False
  '''
  netconf_payload = '''
  	<config>
      <virtual-service-cfg-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-cfg">
        <apps>
          <app>
            <application-name>{application}</application-name>
            <application-network-resource>
              <vnic-gateway-0>0</vnic-gateway-0>
              <virtualportgroup-guest-interface-name-1>0</virtualportgroup-guest-interface-name-1>
              <virtualportgroup-guest-ip-address-1>{ip}</virtualportgroup-guest-ip-address-1>
              <virtualportgroup-guest-ip-netmask-1>{mask}</virtualportgroup-guest-ip-netmask-1>
              <virtualportgroup-application-default-gateway-1>{gateway}</virtualportgroup-application-default-gateway-1>
            </application-network-resource>
          </app>
        </apps>
      </virtual-service-cfg-data>
    </config>	

  '''
  xmlDom = xml.dom.minidom.parseString(str(netconf_connection.edit_config(netconf_payload.format(application=appplication_name, ip=ip, mask=mask, gateway=gateway), target='running')))
  print (xmlDom.toprettyxml( indent = "  " ))
  if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
    return_val = True
  else:
    return_val = False

  return return_val

def verify_app_status(netconf_connection, appplication_name, status="deployed"):
  '''
  This procedure verifies the application status as deployed state. In order to change CPU and memory resources, Application need to be in deployed state.
  '''
  oper_payload = '''
    <filter>
    <virtual-services xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper">
      <virtual-service>
        <name>{application}</name>
        <details>
          <state/>
        </details>
      </virtual-service>
    </virtual-services>
  </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_connection.get(oper_payload.format(application=appplication_name))))
  print(netconf_reply.toprettyxml( indent = "  " ))
  if "<ok/>" not in (netconf_reply.toprettyxml(indent = "  ")):
    return False

  oper_data = XML(netconf_reply.toxml("utf-8"))

  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}virtual-services'):
      for service in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}virtual-service'):
        app_name = service.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}name').text
        print("THIS IS MY APP %s" %app_name)
        for detail in service.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}details'):
          app_status = detail.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}state').text
          if app_status.upper() == status.upper():
            print("Status of application %s is %s as expected" %(app_name, app_status))
            return_val = True
          else:
            print("Status of application %s is not as expected. Expected %s, Actual %s" %(app_name, status, app_status))
            return_val = False

  return return_val
      

if __name__ == '__main__':
    parser = ArgumentParser(description='Select options.')
    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")
    parser.add_argument('-a','--application', type=str,
                        help="Specify the application to be modified")
    parser.add_argument('-i','--ip', type=int, default=12.0.0.2,
                        help="Specify the ip address")
    parser.add_argument('-m','--mask', type=int, default=255.255.255.0,
                        help="Specify the mask")
    parser.add_argument('-g','--gateway', type=int, default=12.0.0.1,
                        help="Specify the default gateway")
    args = parser.parse_args()
    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})


    
    #Step 1. Verify if switch has at least 16.9.1 image running on the box
    if checkversion.verify_sw_version(m, min_major_release=16, min_minor_release=9, min_version=1):
      print("Switch Image meets the required criteria. proceeding with the configuration")
    else:
      print("Switch not ready to configure the feature! Exiting the script")
      exit()

    #Step 2: Verifying if the application is already in deployed state
    if verify_app_status(m, args.application):
      print("Application %s is already deployed. Procedding with changes" %(args.application))
    else:
      print("Application %s not Deployed State ! Exiting!!!" %(args.application))
      exit()

    #Step 3: Modifying the resources
    if modify_app_resources(m, args.application, ip=args.ip, mask=args.mask, gateway=args.gateway):
      print("Resources modified successfully")
    else:
      print("No changes made! Look at configuration")




