#! /usr/bin/env python
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
# This script automates the deployemt of AVB networks. Push all AVB related 
# configurations to multiple switches with single script execution. 
# The automation also handles feature dependencies.

from ncclient import manager
import sys
import time
import xlrd
from IPy import IP

# NETCONF Config Template to use
avb_payload = \
'''<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <avb xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
  </native>
</config>
'''

avb_strict_payload = \
'''<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <avb>
      <strict xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-avb" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
    </avb>
  </native>
</config>
'''

msrp_vlan_payload = \
'''<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <vlan>
      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">
        <id>2</id>
        <name>msrp-vlan</name>
        <state>active</state>
      </vlan-list>
    </vlan>
  </native>
</config>
'''

vtp_payload = \
'''<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <vtp>
          <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vtp">
            <transparent/>
          </mode>
        </vtp>
      </native>
    </config>
'''

mvrp_payload = \
'''<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <mvrp>
      <global xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mvrp" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
      <vlan xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mvrp">
        <create xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
      </vlan>
    </mvrp>
  </native>
</config>
'''

ptp_payload = \
'''<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ptp>
      <profile xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ptp">
        <dot1as xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
      </profile>
      <neighbor-propagation-delay-threshold xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ptp" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge">1500</neighbor-propagation-delay-threshold>
    </ptp>
  </native>
</config>
'''

if __name__ == '__main__':

    program_name = sys.argv[0]
    arguments = sys.argv[1:]
    count = len(arguments)

    if count != 4:
      print("Incorrect Argumnet Count")
      sys.exit()

    try:
      open(sys.argv[1], 'r')
    except OSError:
        print("Incorrect XL file path")
        sys.exit()

    # To open Workbook
    wb = xlrd.open_workbook(sys.argv[1])
    sheet = wb.sheet_by_index(0)

    # For row 0 and column 0
    #print(sheet.nrows)
    #print(sheet.cell_value(2, 1))
 
    # use your user credentials
    USER = sys.argv[2] 
    PASS = sys.argv[3] 

    if sys.argv[4] != 'mvrp_disable' and sys.argv[4] != 'mvrp_enable':
      print(" Incorrect MVRP config status")
      sys.exit()

    #Validate IP address format
    for n in range(1,sheet.nrows):
      IP(sheet.cell_value(n,0))

    #Validate interface # range
    for n in range(1,sheet.nrows):
      list = sheet.cell_value(n,1).split(",")
      list = [ int(x) for x in list ]
      #print('List : ',list)
      for x in list:
        #print(x)
        if x not in range(1,25): #currently hardcoded for 24 port switch
          print("Interface # not within valid range")
          sys.exit()

    for n in range(1,sheet.nrows):
      HOST = sheet.cell_value(n,0)

      netconf_payload = avb_payload
      print ("HOST:",HOST,": ==> Pushing AVB Config")
      #print(netconf_payload)

      with manager.connect(host=HOST, port=830,
                           username=USER,
                           password=PASS,
                           hostkey_verify=False) as m:

          # Send NETCONF <edit-config>
          netconf_reply = m.edit_config(netconf_payload, target="running")

          # Print the NETCONF Reply
          print("REPLY :", netconf_reply)

      netconf_payload = avb_strict_payload
      print ("HOST:",HOST,": ==> AVB STRICT Configuration")
      #print(netconf_payload)

      with manager.connect(host=HOST, port=830,
                           username=USER,
                           password=PASS,
                           hostkey_verify=False) as m:

          # Send NETCONF <edit-config>
          netconf_reply = m.edit_config(netconf_payload, target="running")

          # Print the NETCONF Reply
          print("REPLY :",netconf_reply)

      netconf_payload = msrp_vlan_payload 
      print ("HOST:",HOST,": ==>  MSRP VLAN Configuration")
      #print(netconf_payload)

      with manager.connect(host=HOST, port=830,
                           username=USER,
                           password=PASS,
                           hostkey_verify=False) as m:

          # Send NETCONF <edit-config>
          netconf_reply = m.edit_config(netconf_payload, target="running")

          # Print the NETCONF Reply
          print("REPLY :",netconf_reply)
    
      if sys.argv[4] == 'mvrp_enable':

          netconf_payload = vtp_payload
          print ("HOST:",HOST,": ==> VTP Configuration")
          #print(netconf_payload)

          with manager.connect(host=HOST, port=830,
                               username=USER,
                               password=PASS,
                               hostkey_verify=False) as m:

              # Send NETCONF <edit-config>
              netconf_reply = m.edit_config(netconf_payload, target="running")

              # Print the NETCONF Reply
              print(netconf_reply)


          netconf_payload = mvrp_payload
          print ("HOST:",HOST, ": ==> MVRP Configuration")
          #print(netconf_payload)

          with manager.connect(host=HOST, port=830,
                               username=USER,
                               password=PASS,
                               hostkey_verify=False) as m:

              # Send NETCONF <edit-config>
              netconf_reply = m.edit_config(netconf_payload, target="running")

              # Print the NETCONF Reply
              print("REPLY :",netconf_reply)


      netconf_payload = ptp_payload
      print ("HOST:",HOST, ": ==> PTP Configuration")
      #print(netconf_payload)

      with manager.connect(host=HOST, port=830,
                           username=USER,
                           password=PASS,
                           hostkey_verify=False) as m:

          # Send NETCONF <edit-config>
          netconf_reply = m.edit_config(netconf_payload, target="running")

          # Print the NETCONF Reply
          print("REPLY :",netconf_reply)
      
      list = sheet.cell_value(n,1).split(",")
      list = [ int(x) for x in list ]
    

      #print(netconf_payload)

      with manager.connect(host=HOST, port=830,
                             username=USER,
                             password=PASS,
                             hostkey_verify=False) as m:

        m.lock("running")

        for test in list:

          interface_payload = \
              '''<config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                  <interface>
                    <TenGigabitEthernet>
                      <name>1/0/{}</name>
                      <switchport>
                        <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                          <trunk xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="merge"/>
                        </mode>
                      </switchport>
                    </TenGigabitEthernet>
                  </interface>
                </native>
              </config>
              '''.format(test)


          netconf_payload = interface_payload

          print("    ",HOST,": ==> INTERFACE Config for TenGigabitEthernet 1/0/",test)
              
          # Send NETCONF <edit-config>
          netconf_reply = m.edit_config(netconf_payload, target="running")

          # Print the NETCONF Reply
          print(netconf_reply)
             
        m.unlock("running")
