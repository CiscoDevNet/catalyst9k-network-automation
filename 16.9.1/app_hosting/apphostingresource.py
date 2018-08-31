#!/usr/bin/env python3
#
# Copyright (c) 2018  Sai Zeya <szeya@cisco.com>
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
# This script configures Memory and CPU resources for applictaion which is deployed on Catalyst 9K.



import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
import re
import logging
import checkversion
from xml.etree.ElementTree import XML 



def modify_app_resources(netconf_connection, appplication_name, cpu=80, memory=800):
  '''
  This procedure verifies the application name, CPU resource and Memory resource. 
  Return True if condition satisfied, else return False
  '''
  netconf_payload = '''
   <config>
        <virtual-service-cfg-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-cfg">
          <apps>
            <app>
              <application-name>{application}</application-name>
              <application-resource-profile>
                <profile-name>custom</profile-name>
                <cpu-units xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">{cpu_resource}</cpu-units>
                <memory-capacity-mb xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">{memory_resource}</memory-capacity-mb>
              </application-resource-profile>
            </app>
          </apps>
        </virtual-service-cfg-data>
      </config>
  '''
  xmlDom = xml.dom.minidom.parseString(str(netconf_connection.edit_config(netconf_payload.format(cpu_resource=cpu, memory_resource=memory, application=appplication_name), target='running')))
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
        for detail in service.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}details'):
          app_status = detail.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper}state').text
          if app_status.upper() == status.upper()
            return_val = True
          else:
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
    parser.add_argument('-m','--memory', type=int, default=10,
                        help="Specify the memory value")
    parser.add_argument('-c','--cpu', type=int, default=100,
                        help="Specify the cpu units value")
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
    if modify_app_resources(m, args.application, cpu=args.cpu, memory=args.memory):
      print("Resources modified successfully")
    else:
      print("No changes made! Look at configuration")




