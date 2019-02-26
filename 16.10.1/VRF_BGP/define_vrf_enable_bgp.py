#!/usr/bin/env python3
#
# Copyright (c) 2018, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Raj Kumar Goli'
#__email__ = 'ragoli@cisco.com'
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
# This script defines a vrf, assign an interface to a vrf, configure vpnv4 neighbor and redistribute connected interface of the defined vrf.



"""
    Installing python dependencies:
    > pip install lxml ncclient

    Running script: (save as monitor_errors.py)
    > python3 vrf_config.py --host 172.26.193.176 -u cisco -p cisco --vrf_name test6 --rd_val 6:6 --rt_exp 6:6 --rt_imp 6:6 --int_name TenGigabitEthernet --int_num 1/1/2  --ip_add 11.11.11.1 --sub_mask 255.255.255.0 --local_as 1 --vpn_nei 100.100.100.2 --remote_as 100 --source_lo_num 0 --red_met 10
"""


import sys
import re
import xml.dom.minidom
from argparse import ArgumentParser
from ncclient import manager
from sys import argv
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import XML
import logging


def define_vrf(netconf_handler, vrf_name, rd_val, rt_exp, rt_imp):

    '''This procedure defines a vrf'''

    vrf_payload = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <vrf>
          <definition>
            <name>{vrf_name}</name>
            <rd>{rd_val}</rd>
            <address-family>
              <ipv4>
                <route-target>
                  <export>
                    <asn-ip>{rt_exp}</asn-ip>
                  </export>
                  <import>
                    <asn-ip>{rt_imp}</asn-ip>
                  </import>
                </route-target>
              </ipv4>
            </address-family>
          </definition>
        </vrf>
      </native>
    </config>
    '''

    netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(vrf_payload.format(vrf_name=vrf_name, \
    rd_val=rd_val, rt_exp=rt_exp, rt_imp=rt_imp), target='running')))
    if "<ok/>" in (netconf_reply.toprettyxml(indent=" ")):
        return_val = True
    else:
        return_val = False

    return return_val


def interface_config(netconf_handler, int_name, int_num, vrf_name, ip_add, sub_mask):

    '''This procedure assigns an interface to the vrf with given ip/subnet'''

    int_payload = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <{int_name}>
            <name>{int_num}</name>
            <switchport-conf>
              <switchport>false</switchport>
            </switchport-conf>
            <vrf>
              <forwarding>{vrf_name}</forwarding>
            </vrf>
            <ip>
              <address>
                <primary>
                  <address>{ip_add}</address>
                  <mask>{sub_mask}</mask>
                </primary>
              </address>
            </ip>
          </TenGigabitEthernet>
        </interface>
      </native>
    </config>
    '''
    netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(int_payload.format(int_name=int_name, \
    int_num=int_num, vrf_name=vrf_name, ip_add=ip_add, sub_mask=sub_mask), target='running')))
    if "<ok/>" in (netconf_reply.toprettyxml(indent=" ")):
        return_val = True
    else:
        return_val = False

    return return_val

def vrf_redistribute(netconf_handler, local_as, vrf_name, red_met):
    '''This procedure redistributes connected vrf interfaces into BGP'''

    redistribute_payload = '''
     <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
            <id>{local_as}</id>
            <address-family>
              <with-vrf>
                <ipv4>
                  <af-name>unicast</af-name>
                  <vrf>
                    <name>{vrf_name}</name>
                    <ipv4-unicast>
                      <redistribute>
                        <connected>
                          <metric>{red_met}</metric>
                        </connected>
                      </redistribute>
                    </ipv4-unicast>
                  </vrf>
                </ipv4>
              </with-vrf>
            </address-family>
          </bgp>
        </router>
      </native>
    </config>
    '''

    netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(redistribute_payload.format(local_as=local_as, vrf_name=vrf_name, red_met=red_met), target='running')))
    if "<ok/>" in (netconf_reply.toprettyxml(indent=" ")):
        return_val = True
    else:
        return_val = False
    return return_val

def vpn_neighbor(netconf_handler, local_as, vpn_nei, remote_as, source_lo_num):
    '''This procedude configures vpnv4 neighbor'''

    vpn_neig_payload = '''<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
            <id>{local_as}</id>
            <neighbor>
              <id>{vpn_nei}</id>
              <remote-as>{remote_as}</remote-as>
              <update-source>
                <Loopback>{source_lo_num}</Loopback>
              </update-source>
            </neighbor>
            <address-family>
              <no-vrf>
                <vpnv4>
                  <af-name>unicast</af-name>
                  <vpnv4-unicast>
                    <neighbor>
                      <id>{vpn_nei}</id>
                      <activate/>
                    </neighbor>
                  </vpnv4-unicast>
                </vpnv4>
              </no-vrf>
            </address-family>
          </bgp>
        </router>
      </native>
    </config>
    '''

    netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.edit_config(vpn_neig_payload.format(local_as=local_as, vpn_nei=vpn_nei, remote_as=remote_as, source_lo_num=source_lo_num), target='running')))
    if "<ok/>" in (netconf_reply.toprettyxml(indent=" ")):
        return_val = True
    else:
        return_val = False
    return return_val



if __name__ == '__main__':

    parser = ArgumentParser(description='Select options.')

    # connect to netconf agent

    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify this if you want a non-default port")
    parser.add_argument('--vrf_name', type=str,
                        help="Specify the VRF name")
    parser.add_argument('--rd_val', type=str,
                        help="Specify the rd value for the vrf")
    parser.add_argument('--rt_exp', type=str,
                        help="Specify the rt export for the vrf")
    parser.add_argument('--rt_imp', type=str,
                        help="Specify the rt import for the vrf")
    parser.add_argument('--int_name', type=str,
                        help="Specify the interface name where the vrf has to be configured")
    parser.add_argument('--int_num', type=str,
                        help="Specify the interface number, eg 1/1/2, 1/1/1, etc")
    parser.add_argument('--ip_add', type=str,
                        help="Specify the ip address for the vrf")
    parser.add_argument('--sub_mask', type=str,
                        help="Specify the Subnet mask")
    parser.add_argument('--local_as', type=str,
                        help="Specify the BGP Local AS number")
    parser.add_argument('--vpn_nei', type=str,
                        help="Specify the vpnv4 peering address")
    parser.add_argument('--remote_as', type=str,
                        help="Specify the remote-as for the vpnv4 neighbor")
    parser.add_argument('--source_lo_num', type=str,
                        help="Specify the source interface for the vpnv4 neighbor")
    parser.add_argument('--red_met', type=str,
                        help="Specify the metric for the redistributed routes")
    args = parser.parse_args()

    m = manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         timeout=90,
                         hostkey_verify=False,
                         device_params={'name': 'iosxe'})

    if define_vrf(m, args.vrf_name, args.rd_val, args.rt_exp, args.rt_imp):
        print ("vrf  has been configured") % args.vrf_name
    if interface_config(m, args.int_name, args.int_num, args.vrf_name, args.ip_add, args.sub_mask):
        print("Interface has been configured for the vrf")
    if vrf_redistribute(m, args.local_as, args.vrf_name, args.red_met):
        print ("vrf AF has been enabled and connected routes redistributed")
    if vpn_neighbor(m, args.local_as, args.vpn_nei, args.remote_as, args.source_lo_num):
        print ("VPNV4 neighbor has been configured")
    else:
        print("Config has been been rejected, please investigate")
        exit()
