#!/usr/bin/env python3
#
# Copyright (c) 2019, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Jay Sharma'
#__email__ = 'jayshar@cisco.com'
#__date__ = 'Aug 2019'
#__version__ = 1.0
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

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 
import mdt_oper
import xpath

def configure_mdt_subscription(netconf_handler, subscription_id, subscription_source, subscription_xpath, reciever_addr, reciever_port, reciever_protocol,subscription_encoding='encode-kvgpb',subscription_stream='yang-push',subscription_vrf='', subscription_period=1000):
  '''
    This procedure takes in the netconf handler for the switch and configures 2-event classification on the given interface.
    Procedure returns True if configuration successful, else returns False
    '''

  payload= '''
  <config>
    <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
      <mdt-subscription>
        <subscription-id>{subid}</subscription-id>
        <base>
          <stream>{substream}</stream>
          <encoding>{subencoding}</encoding>
          <source-vrf>{subvrf}</source-vrf>
          <source-address>{subsource}</source-address>
          <period>{subperiod}</period>
          <xpath>{subpath}</xpath>
        </base>
      <mdt-receivers>
        <address>{recieveraddr}</address>
        <port>{recieverport}</port>
        <protocol>{recieverprotocol}</protocol>
      </mdt-receivers>
    </mdt-subscription>
    </mdt-config-data>
  </config>
  '''
    
  print(str((payload.format(subid=subscription_id, substream=subscription_stream, subencoding=subscription_encoding, subvrf=subscription_vrf, subsource=subscription_source, subperiod=subscription_period, subpath=subscription_xpath, recieveraddr=reciever_addr, recieverport=reciever_port, recieverprotocol=reciever_protocol))))
  xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(payload.format(subid=subscription_id, substream=subscription_stream, subencoding=subscription_encoding, subvrf=subscription_vrf, subsource=subscription_source, subperiod=subscription_period, subpath=subscription_xpath, recieveraddr=reciever_addr, recieverport=reciever_port, recieverprotocol=reciever_protocol), target='running')))
  if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
    return_val = True
  else:
    print(xmlDom.toprettyxml(indent = "  "))
    return_val = False

  return return_val
def get_used_subid(netconf_handler):
  '''
    This procedure takes in the netconf handler for the switch and configures 2-event classification on the given interface.
    Procedure returns True if configuration successful, else returns False
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get_config( source='running', filter=('xpath', "/mdt-config-data" ))))
  config = XML(netconf_reply.toxml("utf-8"))
  subscription_id = 1
  for data in config.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for configdata in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg}mdt-config-data'):
      for subscriptions in configdata.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg}mdt-subscription'):
        subscription_id = int(subscriptions.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg}subscription-id').text)

  return subscription_id

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
    parser.add_argument('--sourceaddr', type=str, required=True,
                        help="Specify source address for subscription")
    parser.add_argument('--subscriptiontype', type=str, required=True,
                        help="Specify subscription key from xpath dir")
    parser.add_argument('--subscriptionvrf', type=str, default='Mgmt-vrf',
                        help="Specify subscription vrf")
    parser.add_argument('--encoding', type=str, default='encode-kvgpb',
                        help="Specify subscription encoding")
    parser.add_argument('--stream', type=str, default='yang-push',
                        help="Specify subscription stream")
    parser.add_argument('--period', type=int, default=1000,
                        help="Specify subscription period")
    parser.add_argument('--reciever', type=str, required=True,
                        help="Specify subscription period")
    parser.add_argument('--recieverprotocol', type=str, default='grpc-tcp',
                        help="Specify subscription period")
    parser.add_argument('--recieverport', type=str, default='57500',
                        help="Specify subscription period")
    args = parser.parse_args()
    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})
    available_subid = (get_used_subid(m))+1
    print(configure_mdt_subscription(m, available_subid, args.sourceaddr, xpath.xpathdir[args.subscriptiontype], args.reciever, args.recieverport, args.recieverprotocol,subscription_encoding=args.encoding,subscription_stream=args.stream,subscription_vrf=args.subscriptionvrf, subscription_period=args.period))
    print(mdt_oper.check_reciever_connection(m, args.reciever))
    print(mdt_oper.check_subscription_status(m, available_subid))


