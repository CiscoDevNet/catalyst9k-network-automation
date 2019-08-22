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
