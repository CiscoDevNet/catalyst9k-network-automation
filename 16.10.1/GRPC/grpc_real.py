#!/usr/bin/env python3
#
# Copyright (c) 2018, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Kenny Lei'
#__email__ = 'klei@cisco.com'
#__date__ = 'January 2019'
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
# This script enable Netflow configuration for Encrypted Traffic Analytics Catalyst 9K.
# Limitations:
#  1. The script use the predefine names for NetFlow record (fnf-eta-rec), exporter (fnf-eta-exp) 
#     and monitor (fnf-eta-mon) unless they are specified from the CLI
#  2. Refer to the ETA Cisco Validated Design on cisco.com for eanble ETA on interfaces for differnet deployments



import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
import re
import logging
#import checkversion
from xml.etree.ElementTree import XML 
from jinja2 import Environment , FileSystemLoader


def configure_grpc_subscription(netconf_handler, proc_subid, proc_period, proc_xpath, proc_dstaddr, proc_dstport, proc_srcvrf):

  file_loader = FileSystemLoader('templates')

  env = Environment(loader=file_loader)

  template = env.get_template('grpc_template.j2')
  
  flow_record_payload = template.render(grpc_subid=proc_subid, grpc_period=proc_period, grpc_xpath=proc_xpath, grpc_dstaddr=proc_dstaddr, grpc_dstport=proc_dstport, grpc_srcvrf=proc_srcvrf)

  print(flow_record_payload)

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
    parser.add_argument('--period', type=str, required=True,
                        help="Specify the period for gRPC subscription")
    parser.add_argument('--dst_ipaddr', type=str, required=True,
                        help="Specify the destinaton address for gRPC subscription")
    parser.add_argument('--dst_port', type=str, required=True,
                        help="Specify the destination port for gRPC subscription")
    parser.add_argument('--xpath', type=str, required=True,
                        help="Specify the XPATH for gRPC subscription")
    parser.add_argument('--src_vrf', type=str,
                        help="Specify the XPATH for gRPC subscription")
    args = parser.parse_args()

#    if args.trigger_type  and args.lport is None and args.rport is None:
#        parser.error("--prox requires --lport and --rport.")


    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})


    
    #Step 1. Verify if switch has at least 16.9.1 image running on the box
    #if checkversion.verify_sw_version(m, min_major_release=16, min_minor_release=9, min_version=1):
    #  print("Switch Image meets the required criteria. proceeding with the configuration")
    #else:
    #  print("Switch not ready to configure the feature! Exiting the script")
    #  exit()

    #Step 2: Configure FlowRecord
    if configure_grpc_subscription(m, args.subscription_id, args.period, args.xpath, args.dst_ipaddr, args.dst_port, args.src_vrf):
      print("HURRAAY!! Telemetry subscription has beeen configured.")
    else:
      print("AAARGHH!! Something wrong with configuring the telemetry subscription.")
      exit()

    #
