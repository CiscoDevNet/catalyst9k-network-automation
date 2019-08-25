#!/usr/bin/env python3
#
# Copyright (c) 2019, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Jay Sharma'
#__email__ = 'jayshar@cisco.com'
#__date__ = 'Aug 2019'
#__version__ = 1.0
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
import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import checklicense

def configure_interfacenbar(netconf_handler, interface):
    '''
    Configure nbar on <ifspeed>/<ifname> on switch <netconf_handler>
    '''
    #Parse interface type ane name from <interface>
    interfaceType = re.findall(r'([A-Za-z]+)(\d+/\d+/\d+)', interface)

    payload = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <{interfacespeed}>
            <name>{interfacename}</name>
            <ip>
              <nbar xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-nbar">
                <protocol-discovery/>
              </nbar>
            </ip>
          </{interfacespeed}>
        </interface>
      </native>
    </config>
    '''
    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(payload.format(interfacespeed=interfaceType[0][0], interfacename=interfaceType[0][1]), target='running')))
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
      return_val = True
    else:
      print(xmlDom.toprettyxml(indent = "  "))
      return_val = False

    return return_val

def configure_nbarglobal(netconf_handler):
    '''
    Configure nbar on on switch <netconf_handler> to view on WebUI
    '''
    payload = '''
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <ip>
          <nbar xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-nbar">
            <http-services/>
          </nbar>
        </ip>
      </native>
    </config>
    '''
    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(payload), target='running'))
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
                        help="Interface to configure nbar on")

    args = parser.parse_args()
    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})

    if not checklicense.check_existing_license(m, licensetype='advantage'):
        print("advantage license is mandatory for NBAR! Exiting")
        exit()
    if not configure_interfacenbar(m, args.interface):
        print("Error in configuring NBAR on interface %s" %(args.interface))
        exit()
    if not configure_nbarglobal(m)
        print("Error in configuring NBAR HTTP on switch")
        exit()

