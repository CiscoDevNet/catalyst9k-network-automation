#!/usr/bin/env python3
#
# Copyright (c) 2019, Cisco and/or its affiliates
# All rights reserved.
#__maintainer__ = 'Dimitar Hristov'
#__email__ = 'dhristovi@cisco.com'
#__date__ = 'August 2019'
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
# This script monitors QoS buffer on the SPAN destination interface on Catalyst 9K.i
# it uses CLI: show platform hardware [switch] active qos queue stats interface X/Y/Z
# 
# If the Buffer occupancy grows above 80% the script will remove the SPAN session 
# and try to reconfigure the session again after specified time.
#
# The script is currently ran on Box but it can be used with Off Box as long as connection
# to the device is added and proper credentials
#
# The action to remove/add the SPAN session can be modified to a desired action how to
# react when the buffers are full. For example:
#   1) apply policers
#   2) change Qos Softmax multipler
#   3) change queuing policies
#   4) apply shaping
#   5) etc.
#
# Limitations:
#  1. The script use guestshell os CLIs to generate a syslog message on the console 
#     The script can be linked to EEM script for execution
#
# References
#  2. Refer to the QoS Cisco Validated Design on cisco.com 
#
# Recurring execution can be done via kron job which include the reload of the switch event.
#
# kron policy-list SPAN
#    cli guestshell run python QoS_Microburst.py
#
# kron occurrence SPAN in 1 recurring system-startup
#    policy-list SPAN
#
# To Enable Guestshell:
# 1) iox
# 2) app-hosting appid guestshell
# 3) vnic management guest-interface 0 guest-ipaddress 10.1.3.36 netmask 255.255.255.0  gateway 10.1.3.1
# 4) guestshell enable
# 5) show app-hosting list

import time
import os
import cli
import time
import re

def get_span_sessionID():

# I will use matplotlib to draw the price per day in Boston and Seattle. 
# That require the dataset format to be change from string to integer/float to be able to plot.
# Function "clean_astype_date" converts 'date' to datetime64 type and 'price' to float64

def clean_astype_date(df, price_per_day):

    '''
    INPUT 
        Input on the function will come from CLI execution 
        
    OUTPUT
        Apply regexp to filter the session ID or return 0
    '''
    
    output = cli.execute('show run | in monitor')

    for span_line in output.splitlines():
        p = re.compile(r'^monitor session ([0-9]+).*')
        m = p.match(span_line)
        if m:
            return m.group(1)
    return 0

def get_span_port(span_session):

    '''
    INPUT 
        Input on the function will come from CLI execution using Session ID                               

    OUTPUT
        Apply regexp to filter the interface destination for session ID or return 0
    '''
    

    output = cli.execute('show run | in monitor')
    for span_line in output.splitlines():
        p = re.compile(r'^monitor session [0-9]+ destination interface (.*)')
        m = p.match(span_line)
        if m:
            return m.group(1)

    return 0

def get_span_config():

    '''
    INPUT 
        Input on the function will come from CLI execution                               

    OUTPUT
        Return the monitor session Config or empty 
    '''
    

    output = cli.execute('show run | in monitor')
    span_config = []
    for span_line in output.splitlines():
        span_config.append(span_line)

    return span_config

def delete_span(sessionID):

   '''
   INPUT
       Input on the function is session ID which will be used to delete via CLI

   OUTPUT
       None    
   '''

   cli.configurep("no monitor session \{0\}".format(sessionID))

def span_port_occupancy(span_port):

  '''
  INPUT
      Input on the function will come from CLI execution using the SPAN Port ID

  OUTPUT
       Return the queue real time occupancy per queue for the SPAN port in units. the return is a list. 
  '''

  output = cli.execute('show platform hardware fed active qos queue stats interface {0} | section include [0-9][ ]+[0-9]+.*'.format(span_port))

  queues_only = 0
  All_queues_occupancy = {}
  for queue_buffer in output.splitlines():
      p = re.compile(r'^([0-9]+)[ ]+([0-9]+).*')
      m = p.match(queue_buffer)
      if m:
          Queue_ID = m.group(1)
          occupancy = int(m.group(2))
          All_queues_occupancy.update({Queue_ID : occupancy})

      queues_only = queues_only + 1
      if queues_only == 9:
          break


  return All_queues_occupancy

def span_port_totalbuffer_units(span_port):

  '''
  INPUT
      Input on the function will come from CLI execution using the SPAN Port ID 

  OUTPUT
      Return per queue total number of units give to queue. the return is a list
  '''

  output = cli.execute('show platform hardware fed active qos queue config interface {0} | begin DTS'.format(span_port))

  queues_only = 0
  All_queues_buffers = {}
  for queue_buffer in output.splitlines():
      p = re.compile(r'^[ ]([0-9]+)[ ]+[0-9]+[ ]+[0-9]+[ ]+[0-9]+[ ]+[0-9]+[ ]+([0-9]+).*')
      m = p.match(queue_buffer)

      if m:
          Queue_ID = m.group(1)
          Buffers = int(m.group(2))
          All_queues_buffers.update(\{Queue_ID : Buffers\}) 

      queues_only = queues_only + 1
      if queues_only == 11:
          break


  return All_queues_buffers


if __name__ == '__main__':

   # Get SPAN Config in case we need to reconfigure it back
   span_config = get_span_config()

   # Get SPAN Session Port
   span_port = get_span_port(get_span_sessionID)

   # Get SPAN Session ID
   sessionID = get_span_sessionID() 

   # Substract and find the difference between total and occupied. If the occupancy per queue is more than 80% remove the SPAN
   d1 = span_port_totalbuffer_units(span_port)
   d2 = span_port_occupancy(span_port)
   for k, v in d1.items():
      if v > 0:
         cmd = "echo " + "\'a Queue is Occupied above 80%: {0} \'".format(float(d2.get(k, 0))/float(v)) + " > /dev/ttyS2"
         os.system(cmd)
         time.sleep(2)
         if float(d2.get(k, 0))/float(v) > 0.8:
             cmd = "echo " + "\'Deleting SPAN session with ID: {0} \'".format(sessionID) + " > /dev/ttyS2"
             os.system(cmd)
             time.sleep(2)
             delete_span(sessionID)
             cmd = "echo " + "\'Session is Deleted\'" + " > /dev/ttyS2"
             os.system(cmd)
             time.sleep(2)

             break

   cmd = "echo " + "\'Waiting for 20 secs\'" + " > /dev/ttyS2"
   os.system(cmd)
   time.sleep(20)

   # Reconfigure the session after 20 seconds as the Microburst condition might have disappeared.
   cmd = "echo " + "\'Reconfigure the SPAN session with ID: {0}\'".format(sessionID) + " > /dev/ttyS2"
   os.system(cmd)

   cli.configurep(span_config)
