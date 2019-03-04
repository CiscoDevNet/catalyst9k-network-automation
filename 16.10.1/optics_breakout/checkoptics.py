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
# This script retrieves software version from the switch and verifies whether the switch meets the expected version critertion

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 



def verify_sw_version(netconf_handler, min_major_release=16, min_minor_release=9, min_version=1):

  '''
  This procedure verifies whether the software version of the switch with <netconf_handler>is greater than or equal to given <min_sw_version> 
  Return True if condition satisfied, else return False
  '''

  payload = '''
    <filter>
      <device-hardware-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper">
        <device-hardware>
          <device-system-data>
            <boot-time/>
            <software-version/>
          </device-system-data>
        </device-hardware>
      </device-hardware-data>
    </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload)))

  oper_data = XML(netconf_reply.toxml("utf-8"))

  print(netconf_reply.toprettyxml(indent = "  "))

  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-hardware-data'):
      for device in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-hardware'):
        for sysdata in device.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-system-data'):
            sw_version = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}software-version').text
            print(sw_version)

  release = re.findall(r'^.*Version (\d+)\.(\d+)\.(\d+)', sw_version, re.MULTILINE)
  if (int(release[0][0])>= int(min_major_release)) and (int(release[0][1]) >= int(min_minor_release)) and (int(release[0][2]) >= int(min_version)):
    return_val = True
  else:
    print("Sofware version currently running: %s minimum expected release %s.%s.%s" %(release,min_major_release, min_minor_release, min_version))
    return_val = False

  return return_val

def verify_optics_support(netconf_handler):
  opticDict ={}
  payload = '''
     <filter>
      <device-hardware-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper">
        <device-hardware>
          <device-inventory/>
        </device-hardware>
      </device-hardware-data>
    </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload)))

  oper_data = XML(netconf_reply.toxml("utf-8"))
  transcieverexists = False
  transcieverList = []
  print(netconf_reply.toprettyxml(indent = "  "))
  
  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-hardware-data'):
      for device in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-hardware'):
        for inventory in device.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}device-inventory'):
            hw_type = inventory.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}hw-type').text
            if hw_type == 'hw-type-transceiver':
              transciever_name = inventory.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}part-number').text.strip()
              transceiver_desc = inventory.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper}hw-description').text.strip()
              opticDict[transceiver_desc] = transciever_name

  return opticDict



def transciever_oper(netconf_handler, interfaceName, opticDict, opticsfile):
  payload = '''
      <filter>
      <transceiver-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-transceiver-oper">
        <transceiver>
          <name>{itf}</name>
        </transceiver>
      </transceiver-oper-data>
    </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload.format(itf=interfaceName))))
  transcieverSupported = False
  opticfile = open(opticsfile, "r")
  oper_data = XML(netconf_reply.toxml("utf-8"))
  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-transceiver-oper}transceiver-oper-data'):
      for transceiver in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-transceiver-oper}transceiver'):
        optic = transceiver.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-transceiver-oper}ethernet-pmd').text
        print("optic is %s" %optic)

  optic_name = opticDict[optic]
  for opt in opticfile:
    #print("%s, %s" %(opt.strip(), optic_name))
    if optic_name == opt.strip():
      transcieverSupported = True
      break

  print(optic_name)
  return transcieverSupported

def verify_interface_support(interfaceName):
  interfaceType = re.findall(r'([A-Za-z]+)\d+/\d+/(\d+)', interfaceName)
  if int(interfaceType[0][1])%4 == 0:
    supported = False
  else:
    supported = True

  return supported

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
  parser.add_argument('-name', '--name', type=str, default='NCLIENT',
                      help="hostname for the device! ;-)")
  args = parser.parse_args()
  m =  manager.connect(host=args.host,
                       port=args.port,
                       username=args.username,
                       password=args.password,
                       device_params={'name':"iosxe"})
  opt_dict = (verify_optics_support(m))
  print(transciever_oper(m, "HundredGigE1/0/1", opt_dict, "supportedoptic.txt"))
  print(verify_sw_version(m, min_major_release=16, min_minor_release=10, min_version=1))
  print(verify_interface_support("HundredGigE1/0/12"))
