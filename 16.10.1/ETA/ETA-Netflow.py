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
import checkversion
from xml.etree.ElementTree import XML 


def configure_flow_record(netconf_handler, proc_recordname, proc_exportername, proc_exporter_ip, proc_exporter_port, proc_monitorname):
  '''
  This procedure configure Netflow record for ETA
  '''
  flow_record_payload = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <flow>
          <record xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-flow">
            <name>{eta_record}</name>
            <description>For ETA</description>\
            <collect>
              <counter>
                <bytes>
                  <long/>
                </bytes>
                <packets>
                  <long/>
                </packets>
              </counter>
              <timestamp>
                <absolute>
                  <first/>
                  <last/>
                </absolute>
              </timestamp>
            </collect>
            <match>
              <ipv4>
                <destination>
                  <address/>
                </destination>
                <protocol/>
                <source>
                  <address/>
                </source>
              </ipv4>
              <transport>
                <destination-port/>
                <source-port/>
              </transport>
            </match>
          </record>
          <exporter xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-flow">\
            <name>{eta_exporter}</name>\
            <description>For ETA</description>\
            <destination>\
              <ipdest>\
                <ip>{eta_exporter_ip}</ip>\
              </ipdest>\
            </destination>\
            <transport>\
              <udp>{eta_exporter_port}</udp>\
            </transport>\
          </exporter>\
          <monitor xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-flow">\
            <name>{eta_monitor}</name>\
            <description>For ETA</description>\
            <cache>\
              <timeout>\
                <active>60</active>\
              </timeout>\
            </cache>\
            <exporter>\
              <name>{eta_exporter}</name>\
            </exporter>\
            <record>\
              <type>{eta_record}</type>\
            </record>\
          </monitor>\
        </flow>
      </native>
    </config>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(flow_record_payload.format(eta_record=proc_recordname, eta_exporter=proc_exportername, eta_exporter_ip=proc_exporter_ip, eta_exporter_port=proc_exporter_port, eta_monitor=proc_monitorname), target='running')))
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
    parser.add_argument('--recordname', type=str, default='fnf-eta-rec',
                        help="Specify the NetFlow Record name for ETA")
    parser.add_argument('--exportername', type=str, default='fnf-eta-exp',
                        help="Specify the NetFlow exporter name for ETA")
    parser.add_argument('--exporterip', type=str, required=True,
                        help="Specify the NetFlow exporter IP")
    parser.add_argument('--exporterudpport', type=int, default=2055,
                        help="Specify the NetFlow UDP port number for ETA")
    parser.add_argument('--monitorname', type=str, default='fnf-eta-mon',
                        help="Specify the NetFlow Monitor name for ETA")
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

    #Step 2: Configure FlowRecord
    if configure_flow_record(m, args.recordname, args.exportername, args.exporterip, args.exporterudpport, args.monitorname):
      print("Configured")
    else:
      print("Something wrong with configuring NetFlow for ETA")
      exit()

    #
