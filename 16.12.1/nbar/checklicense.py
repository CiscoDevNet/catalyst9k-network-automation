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
import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML

def check_existing_license(netconf_handler, licensetype='essential'):
  '''
    This procedure takes in the netconf handler for the switch and configures 2-event classification on the given interface.
    Procedure returns True if configuration successful, else returns False
  '''
  licenseVaildated = False
  output = (str(netconf_handler.get_config( source='running', filter=('xpath', "/native/license"))))
  netconf_reply = xml.dom.minidom.parseString(str(netconf_handler.get_config( source='running', filter=('xpath', "/native/license" ))))
  config = XML(netconf_reply.toxml("utf-8"))
  for data in config.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
  	for native in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}native'):
  		for license in native.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}license'):
  			for boot in license.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}boot'):
  				for level in boot.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-native}level'):
  					for lictype in level:
  						if licensetype in str(lictype.tag):
  							licenseVaildated = True
  if licenseVaildated:
  	return_val = True
  else:
  	print("license not validated. Output %s" %output)
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
    args = parser.parse_args()
    m =  manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})
    print(check_existing_license(m))