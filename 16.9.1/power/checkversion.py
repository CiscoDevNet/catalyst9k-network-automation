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
