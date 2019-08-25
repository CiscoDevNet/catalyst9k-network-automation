#!/usr/bin/env python3
#
# Copyright (c) 2019, Cisco and/or its affiliates
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
# This script retrieves model driven telmetry oper data

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 

def check_reciever_connection(netconf_handler, reciever_ip, status='active'):

  '''
  This procedure verifies whether the status to <reciever_ip> from the switch with <netconf_handler>
  Return True if condition satisfied, else return False
  '''

  payload = '''
    <filter>
      <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
        <mdt-subscriptions>
          <mdt-receivers/>
        </mdt-subscriptions>
      </mdt-oper-data>
    </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload)))

  oper_data = XML(netconf_reply.toxml("utf-8"))

  print(netconf_reply.toprettyxml(indent = "  "))

  return_val = False
  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for subscriptions in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}mdt-oper-data'):
      for recievers in subscriptions.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}mdt-subscriptions'):
        for sysdata in recievers.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}mdt-receivers'):
            recieverip = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}address').text
            recieverport = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}port').text
            recieverprotocol = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}protocol').text
            recieverstate = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}state').text
            if recieverip == reciever_ip:
              if status == 'active':
                if recieverstate == 'rcvr-state-connected':
                  return_val = True
              else:
                if recieverstate != 'rcvr-state-connected':
                  return_val = True

  return return_val

def check_subscription_status(netconf_handler, subscription_id, status='valid'):

  '''
  This procedure verifies whether the subscription <subscription_id> exists on the switch with <netconf_handler>
  Return True if <subscription_id> status matches the status, else return False
  '''

  payload = '''
    <filter>
      <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
        <mdt-subscriptions>
          <subscription-id>{subscription_number}</subscription-id>
        </mdt-subscriptions>
      </mdt-oper-data>
    </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get(payload.format(subscription_number=subscription_id))))

  oper_data = XML(netconf_reply.toxml("utf-8"))

  print(netconf_reply.toprettyxml(indent = "  "))

  return_val = False
  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for subscriptions in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}mdt-oper-data'):
      for subscription in subscriptions.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}mdt-subscriptions'):
        subid = subscription.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}subscription-id').text
        print("subscription id is %s" %subid)
        for sysdata in subscription.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}base'):
          substream = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}stream').text
          subencoding = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}encoding').text
          subsource_vrf = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}source-vrf').text
          subsource_address = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}source-address').text
          subxpath_used = sysdata.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}xpath').text
        subtype = subscription.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}type').text
        substate = subscription.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper}state').text
        #print(subid, substream, subencoding, subsource_vrf, subsource_address, subxpath_used, subtype, substate, status)

  if status =='valid' and substate == 'sub-state-valid':
      return_val = True
  elif status == 'invalid' and substate == 'sub-state-invalid':
      return_val = True

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
    args = parser.parse_args()
    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})
    check_reciever_connection(m, "172.26.211.58")
    check_subscription_status(m, '501', status='valid')
