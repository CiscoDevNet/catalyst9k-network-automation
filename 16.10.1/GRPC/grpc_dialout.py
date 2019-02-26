#!/usr/bin/env python3
#
# Copyright (c) 2018, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Siddharth Krishna'
#__email__ = 'sidkrish@cisco.com'
#__date__ = 'February 2019'
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
#
# This script automates streaming telemetry grpc (dial-out) based subscription on the Catalyst 9K.
# It uses Jinja Templates for dynamic redering of XML payloads to netconf requests. 



import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
import re
import logging
#import checkversion
from xml.etree.ElementTree import XML 
from jinja2 import Environment , FileSystemLoader


def configure_grpc_subscription(netconf_handler, proc_subid, proc_triggertype, proc_period, proc_xpath, proc_dstaddr, proc_dstport, proc_srcaddr, proc_srcvrf):

  file_loader = FileSystemLoader('templates')

  env = Environment(loader=file_loader)

  template = env.get_template('grpc_template.j2')
  
  flow_record_payload = template.render(grpc_subid=proc_subid, grpc_trigger_type= proc_triggertype, grpc_period=proc_period, grpc_xpath=proc_xpath, grpc_dstaddr=proc_dstaddr, grpc_dstport=proc_dstport, grpc_srcaddr=proc_srcaddr, grpc_srcvrf=proc_srcvrf)

  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(flow_record_payload, target='running')))
  print (netconf_reply.toprettyxml( indent = "  " ))
  if "<ok/>" in (netconf_reply.toprettyxml(indent = "  ")):
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
    parser.add_argument('--subscription_id', type=str, required=True,
                        help="Specify the id for gRPC subscription")
    parser.add_argument('--trigger_type', type=str, required=True,
                        help="Specify the trigger type for gRPC subscription - must be either 'onchange' or 'periodic'")
    parser.add_argument('--period', type=str,
                        help="Specify the period for gRPC subscription - must for trigger type 'periodic'")
    parser.add_argument('--dst_ipaddr', type=str, required=True,
                        help="Specify the destinaton address for gRPC subscription")
    parser.add_argument('--dst_port', type=str, required=True,
                        help="Specify the destination port for gRPC subscription")
    parser.add_argument('--xpath', type=str, required=True,
                        help="Specify the XPATH for gRPC subscription")
    parser.add_argument('--src_ipaddr', type=str,
                        help="Optional,Specify the switch source address for gRPC subscription")
    parser.add_argument('--src_vrf', type=str,
                        help="Optional, Specify the switch source VRF for gRPC subscription")
    args = parser.parse_args()
  
    if args.trigger_type != 'periodic' and args.trigger_type != 'onchange':
        parser.error("--trigger_type must be either 'onchnage' or 'periodic'")

    if args.trigger_type == 'periodic' and args.period is None:
        parser.error("'--trigger_type periodic needs a valid period value'")


    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})


    
    if configure_grpc_subscription(m, args.subscription_id, args.trigger_type, args.period, args.xpath, args.dst_ipaddr, args.dst_port, args.src_ipaddr, args.src_vrf):
      print("HURRAAY!! Telemetry subscription has beeen configured.")
    else:
      print("AAARGHH!! Something wrong with configuring the telemetry subscription.")
      exit()
