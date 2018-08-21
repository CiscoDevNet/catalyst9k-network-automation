#!/usr/bin/env python3
#
# Copyright (c) 2018  Jay Sharma <jayshar@cisco.com>
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
# This script configures two event classification on a switch via NETCONF

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 
import checkversion

def configure_two_event_classification(netconf_handler, interface):
  '''
  This procedure takes in the netconf handler for the switch and configures 2-event classification on the given interface.
  Procedure returns True if configuration successful, else returns False
  '''

  two_event_payload = '''
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <interface>
        <{interface_type}>
          <name>{interface_number}</name>
          <power xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-power">
          <inline>
              <port>
                <two-event/>
              </port>
            </inline>
          </power>
        </{interface_type}>
      </interface>
    </native>
  </config>
  '''

  #Parse interface type ane name from <interface>
  interfaceType = re.findall(r'([A-Za-z]+)(\d+/\d+/\d+)', interface)

  #Verify if Two event classification is already configured
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get_config( source='running', filter=('xpath', "/native/interface/%s[name='%s']/power" %(interfaceType[0][0], interfaceType[0][1])))))
  print(netconf_reply.toprettyxml( indent = "  " ))

  config = XML(netconf_reply.toxml("utf-8"))

  alreadyConfigured = False

  for data in config.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for native in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}native'):
      for interface in native.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}interface'):
        for itftype in interface.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}%s'%(interfaceType[0][0])):
          for power in itftype.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-power}power'):
            for inline in power.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-power}inline'):
              for port in inline.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-power}port'):
                for iter in port:
                  if "two-event" in iter.tag:
                    print("Two event classification is already cofigured on the port")
                    alreadyConfigured = True
            
  #If already configured, exit. Else continue with configuration
  if alreadyConfigured:
    return_val = True
  else:
    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(two_event_payload.format(interface_type=interfaceType[0][0], interface_number=interfaceType[0][1]), target='running')))
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
      return_val = True
    else:
      print(xmlDom.toprettyxml(indent = "  "))
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
    parser.add_argument('-i', '--interface', type=str,
                        help="Interface to configure 2 event classification on")
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

    #Step 2. Configure Perpetual PoE on the interface
    if configure_two_event_classification(m, args.interface):
      print("Succesfully configured 2 event classification")
    else:
      print("configuration failed!")