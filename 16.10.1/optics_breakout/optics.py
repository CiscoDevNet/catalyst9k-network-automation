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
# This script retrieves hostname from user and configures on the switch via NETCONF  
# prints the response from the switch out in a "pretty" XML tree.

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 
import checkoptics

def configure_port_breakout(netconf_handler, interface):
  '''
  This procedure takes in the netconf handler for the switch and configures 2-event classification on the given interface.
  Procedure returns True if configuration successful, else returns False
  '''

  port_breakout = '''
 <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hw-module>
          <breakout>
            <port-number xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">{port_number}</port-number>
          </breakout>
        </hw-module>
      </native>
    </config>
  '''

  #Parse interface type ane name from <interface>
  interfaceType = re.findall(r'([A-Za-z]+)\d+/\d+/(\d+)', interface)
  xmlDom = xml.dom.minidom.parseString(str( m.edit_config(port_breakout.format(port_number=interfaceType[0][1]), target='running')))
  if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
      return_val = True
  else:
    print(xmlDom.toprettyxml(indent = "  "))
    return_val = False

  return return_val


def verify_optics_configuration(netconf_handler, main_interface):
  payload = '''
      <filter>
      <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper">
        <interface>
          <name>{itf}</name>
        </interface>
      </interfaces>
    </filter>
  '''
  breakout_interface = main_interface + "/2"
  
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload.format(itf=breakout_interface))))
  oper_data = XML(netconf_reply.toxml("utf-8"))

  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper}interfaces'): 
      for intf in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper}interface'):
        itf_name = intf.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper}name').text

  print(itf_name)
  try:
    if itf_name == breakout_interface:
      return_val = True

  except:
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
                      help="Yep, this one too!")
  parser.add_argument('--port', type=int, default=830,
                      help="Specify this if you want a non-default port")
  parser.add_argument('-i', '--interface', type=str, default='NCLIENT',
                      help="Interface on the device to configure breakout")
  parser.add_argument('-f', '--opticsfile', type=str, default='supportedoptic.txt',
                      help="optics file that contains list of supported breakout optics")
  args = parser.parse_args()
  m =  manager.connect(host=args.host,
                       port=args.port,
                       username=args.username,
                       password=args.password,
                       device_params={'name':"iosxe"})


  print("Checking optics present on the switch from its inventory")

  opt_dict = checkoptics.verify_optics_support(m)

  print(opt_dict)

  print("Checking if the optics connected to target interface support breakout using the breakout list")

  transcieverSupported = checkoptics.transciever_oper(m, args.interface, opt_dict, args.opticsfile)
  if not transcieverSupported:
    print("Transciever connected on target port is not supported!")
    exit()

  print("Checking if the optics connected is supported on the software version")

  softwareSupported = checkoptics.verify_sw_version(m, min_major_release=16, min_minor_release=10, min_version=1)


  if not softwareSupported:
    print("Software version is not supported! Please check.")
    exit()

  print("Checking if the given interface supports breakout")

  interfaceSupported= checkoptics.verify_interface_support(args.interface)
  if not interfaceSupported:
    print("Interface is not supported with breakout! Please check.")
    exit()

  print("Configuring breakout")

  configPassed = configure_port_breakout(m, args.interface)
  if not configPassed:
    print("Configuring breakout failed!")
    exit()

  print("Verifying breakout configuration")

  verified = verify_optics_configuration(m, args.interface)

  if not verified:
    print("Could not verify successful configuration of breakout")
    exit()

  print("Successfully configured breakout")
