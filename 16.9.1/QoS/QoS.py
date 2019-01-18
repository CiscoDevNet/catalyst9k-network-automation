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
# This script configures fast PoE on the interface provided by the user via NETCONF

# Sample Usage:
#
# Start The script
# virtual-machine:~$ python3 QoS.py --host 172.26.197.51
#
# The script will open a new prompt": Enter "help" to see the options
# 
# Starting QoSPolicy prompt...
# QoSPolicy> help
#
# Documented commands (type help <topic>):
# ========================================
# add_class_map_to_policy        class_map  show_class_map  
# attach_policy_under_interface  help       show_policy_map 
# change_softmax                 quit       show_qos_softmax
#
# Enter "show_qos_softmax" to read the value from the device
# Then enter "change_softmax" to change it
# 
# QoSPolicy> show_qos_softmax
# 300
# QoSPolicy> change_softmax
# Enter softmax value
# > 1200
# Successfully configured SoftMax
# QoSPolicy> show_qos_softmax
# 1200
#
# 
# Read the Class-maps configured on the device
# Then enter show_policy_map to see what class-maps are allocated to the policy and add a new class-map via "add_class_map_to_policy"
#
# QoSPolicy> show_class_map
# ['Test', 'Test1', 'cMAP', 'cMAP_40']
# QoSPolicy> show_policy_map
# ['Policy map: InputPolicy  Contains Class maps: Test  cMAP  ']
# QoSPolicy> add_class_map_to_policy 
# Enter Class-map Name
# > cMAP_40
# Enter DSCP value to set in Class-map
# > 34
# Enter Policy-map Name
# > InputPolicy
# Successfully configured Class-Map cMAP_40 with set action DSCP 34 under Policy-Map InputPolicy
# QoSPolicy> show_policy_map
# ['Policy map: InputPolicy  Contains Class maps: Test  cMAP  cMAP_40  ']
#
#
#
# Attach policy-map to interface via "attach_policy_under_interface". The interface name syntax matter hence please spell it as defined.
#
# QoSPolicy> attach_policy_under_interface
# Enter Interface Name one from FastEthernet or GigabitEthernet or TenGigabitEthernet
# > GigabitEthernet1/0/2
# Enter Policy-map Name
# > InputPolicy
# Enter Policy-map Direction
# > input
# Successfully configured input Policy-Map InputPolicy under interface GigabitEthernet1/0/2
# QoSPolicy> 

#switch config prequisutes
#netconf-yang

import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom
from xml.etree.ElementTree import XML
import re
import logging 
from cmd import Cmd
from xml.etree.ElementTree import XML, fromstring, tostring
import xml.etree.ElementTree as ET
import xmltodict

def configure_qos_softmax(netconf_handler,softmax):
    '''
    This procedure takes in the netconf handler for the switch and configures QoS SoftMAx Multiplier which is global CMD
    Procedure returns True if configuration successful, else returns False
    '''

    qos_softmax_payload = \
    ''' <config>
         <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
           <qos>
             <queue-softmax-multiplier xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-qos">
               <value>{softmax}</value>
             </queue-softmax-multiplier>
           </qos>
         </native>
        </config>
    ''' 

    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(\
             qos_softmax_payload.format(softmax=softmax), \
             target='running')))
    
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
       return_val = True
    else:
       print(xmlDom.toprettyxml(indent = "  "))
       return_val = False

    return return_val

def configure_qos_class_map(netconf_handler, class_map_name, class_map_match):
    '''
    This procedure takes in the netconf handler for the switch and configures QoS Class-Map
    Procedure returns True if configuration successful, else returns False
    '''

    class_map_payload = \
    ''' <config>
         <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <policy>
              <class-map xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-policy">
                <name>{class_map_name}</name>
                <prematch>match-all</prematch>
                <match>
                  <dscp>{class_map_match}</dscp>
                </match>
              </class-map>
            </policy>
         </native>
        </config>
    '''

    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(\
             class_map_payload.format(class_map_name=class_map_name, class_map_match=class_map_match), \
             target='running')))
    
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
       return_val = True
    else:
       print(xmlDom.toprettyxml(indent = "  "))
       return_val = False

    return return_val

def configure_qos_policy_map(netconf_handler, policy_map_name, class_map_name, class_map_set):
    '''
    This procedure takes in the netconf handler for the switch and configures QoS Policy-Map
    Procedure returns True if configuration successful, else returns False
    '''

    policy_map_payload = \
    ''' <config>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <policy>
              <policy-map xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-policy">
                <name>{policy_map_name}</name>
                <class>
                  <name>{class_map_name}</name>
                  <action-list>
                    <action-type>set</action-type>
                    <set>
                      <dscp>
                        <dscp-val>{class_map_set}</dscp-val>
                      </dscp>
                    </set>
                  </action-list>
                </class>
              </policy-map>
            </policy>
         </native>
        </config>
    '''

    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(policy_map_payload.format(\
             policy_map_name=policy_map_name, class_map_name=class_map_name, class_map_set=class_map_set), \
             target='running')))
    
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
      return_val = True
    else:
      print(xmlDom.toprettyxml(indent = "  "))
      return_val = False

    return return_val


def attach_qos_policy_map(netconf_handler, interface, policy_map_direction, policy_map_name):
    '''
    This procedure takes in the netconf handler for the switch and attaches QoS Policy-Map to Interface
    Procedure returns True if configuration successful, else returns False
    '''

    #Parse interface type and name from <interface>
    interfaceType = re.findall(r'([A-Za-z]+)(\d+/\d+/\d+)', interface)

    interface_policy_payload = \
    ''' <config>
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
              <{interface_type}>
                <name>{interface_number}</name>
                <service-policy xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-policy">
                  <{policy_map_direction}>{policy_map_name}</{policy_map_direction}>
                </service-policy>
              </{interface_type}>
            </interface>
          </native>
        </config>
    '''

    xmlDom = xml.dom.minidom.parseString(str(netconf_handler.edit_config(interface_policy_payload.format(interface_type=interfaceType[0][0], interface_number=interfaceType[0][1], \
             policy_map_direction=policy_map_direction, policy_map_name=policy_map_name), target='running')))
    
    if "<ok/>" in (xmlDom.toprettyxml(indent = "  ")):
      return_val = True
    else:
      print(xmlDom.toprettyxml(indent = "  "))
      return_val = False

    return return_val


def get_qos_softmax(netconf_handler):
    '''
    This procedure takes in the netconf handler for the switch and read what is the QoS Softmax Multiplier
    Procedure returns True if configuration successful, else returns False
    '''

    netconf_reply = netconf_handler.get_config( source='running', filter=('xpath', "/native/qos/queue-softmax-multiplier/value"))
    data = xmltodict.parse(netconf_reply.xml)
   
    return (data["rpc-reply"]["data"]["native"]["qos"]["queue-softmax-multiplier"]["value"])

def get_qos_class_map(netconf_handler):
    '''
    This procedure takes in the netconf handler for the switch and read what is the QoS Softmax Multiplier
    Procedure returns True if configuration successful, else returns False
    '''

    netconf_reply = netconf_handler.get_config( source='running', filter=('xpath', "/native/policy/class-map"))

    data = xmltodict.parse(netconf_reply.xml)
    #print (data)
   
    class_map_names = [] 
    for cmap in (data["rpc-reply"]["data"]["native"]["policy"]["class-map"]):
        class_map_names.append(cmap["name"])


    return class_map_names

def get_qos_policy_map(netconf_handler):
    '''
    This procedure takes in the netconf handler for the switch and read what is the QoS Softmax Multiplier
    Procedure returns True if configuration successful, else returns False
    '''

    netconf_reply = netconf_handler.get_config( source='running', filter=('xpath', "/native/policy/policy-map"))

    data = xmltodict.parse(netconf_reply.xml)

    policy_map_names = [] 
    for pmap in (data["rpc-reply"]["data"]["native"]["policy"]["policy-map"]):
        if (pmap["name"]) != "system-cpp-policy":
            class_maps_in_policy = "  Contains Class maps: " 
            for cmap in (pmap["class"]):
                class_maps_in_policy = class_maps_in_policy + cmap["name"] + "  "
            policy_map_names.append("Policy map: " + pmap["name"] + class_maps_in_policy) 

    return policy_map_names 

class QoSPolicy(Cmd):

    def do_class_map(self, args):
        """Defines Class-map and match criteria """
	
        global m

        print ("Enter Class-map Name")
        class_map_name = input('> ')

        print ("Enter DSCP value to match")
        class_map_match = input('> ')

        if configure_qos_class_map(m, class_map_name, class_map_match): 
          print("Successfully configured Class-Map %s which matches %s" %(class_map_name, class_map_match))
        else:
         print("configuration failed!")
        
    def do_add_class_map_to_policy(self, args):
        """ Add a new Class-Map under Policy-Map """

        global m

        print ("Enter Class-map Name")
        class_map_name = input('> ')

        print ("Enter DSCP value to set in Class-map")
        class_map_set = input('> ')

        print ("Enter Policy-map Name")
        policy_map_name = input('> ')

        if configure_qos_policy_map(m, policy_map_name, class_map_name, class_map_set): 
          print("Successfully configured Class-Map %s with set action DSCP %s under Policy-Map %s" %(class_map_name, class_map_set, policy_map_name))
        else:
          print("configuration failed!")       
        
    def do_attach_policy_under_interface(self, args):
        """ attaches a policy-map under Interface """
       
        global m

        print ("Enter Interface Name one from FastEthernet or GigabitEthernet or TenGigabitEthernet")
        interface = input('> ')

        print ("Enter Policy-map Name")
        policy_map_name = input('> ')

        print ("Enter Policy-map Direction")
        policy_map_direction = input('> ')

        if attach_qos_policy_map(m, interface, policy_map_direction, policy_map_name): 
          print("Successfully configured %s Policy-Map %s under interface %s" %(policy_map_direction, policy_map_name, interface))
        else:
          print("configuration failed!") 

        
    def do_show_class_map(self, args):
        """ show class map content """
       
        global m
        print (get_qos_class_map(m))       
 
    def do_show_policy_map(self, args):
        """ show policy map content """
       
        global m
        print (get_qos_policy_map(m)) 


    def do_show_qos_softmax(self, args):
        """ show policy map content """

        global m
        print (get_qos_softmax(m)) 
 
    def do_change_softmax(self, args):
        """ Change Softmax buffer Multiplier """

        global m

        print ("Enter softmax value")
        softmax = input('> ')

        if configure_qos_softmax(m,softmax): 
          print("Successfully configured SoftMax")
        else:
          print("configuration failed!")

    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit

if __name__ == '__main__':

    parser = ArgumentParser(description='Select NETCONF connection options.')
    
    # Input parameters
    parser.add_argument('--host', type=str, required=True,
                        help="The device IP or DN")
    parser.add_argument('-u', '--username', type=str, default='cisco',
                        help="Go on, guess!")
    parser.add_argument('-p', '--password', type=str, default='cisco',
                        help="Yep, this one too! ;-)")
    parser.add_argument('--port', type=int, default=830,
                        help="Specify non-default port for NETCONF")


    args = parser.parse_args()

    global m 
    m = manager.connect(host=args.host,
                         port=args.port,
                         username=args.username,
                         password=args.password,
                         device_params={'name':"iosxe"})



    prompt = QoSPolicy()
    prompt.prompt = 'QoSPolicy> '
    prompt.cmdloop('Starting QoSPolicy prompt...')



