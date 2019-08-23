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
# 
# This script is use to Automate the process to register devices to on premise 
# CSSM Satellite. 
#
# It requires to have:
# 1) a valid ID Token from the Satellite
# 2) Satellite IP address that will be used to register
# 3) Port 80 to the satellite should be open
# 4) if a VRF is used modify the Call-home and the source interface for HTTP Client
# 5) User credentials to login towards the device
#
# The script is written to be run off Box. So it can register multiple Device.
# The script can be modified to use a list of device to register them at once.
#
#####

# import the requests library
import sys
import json
import paramiko
import time
import re
import datetime

# use the IP address or hostname of your switch
HOST_SW = '172.26.197.70'

# use your user credentials to access the switch
USER_SW = 'cisco'
PASS_SW = 'cisco'

SatIP = "172.26.197.111"
SatPort = "80"
token = "NzE4MDNmYTMtNTZlOC00MGU2LTgzZGUtOGFkOGViNWQ0YjhiLTE1NzIxMTM0%0AMjQ1MzJ8b21XT0JTU21WbExKVGR1c1lyakdxTU82Z29icC80WFhXcGFBblNO%0AbC9rbz0%3D%0A"

def Config_Profile(conn, SatIP, SatPort):

    '''
    INPUT
        conn - Connection Handle that will be used to login the switch
        SatIP - Satellite IP to use into Call Home
        SatPort - it is pre set to 80 but it can be custom modified if changed on the satellite

    OUTPUT
        Deacticate the default CiscoTAC-1 profile and configure a new one that points 
        toward the Satellite
    '''
    
    conn.send("configure terminal\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("call-home\n")
    time.sleep(2)
    output = conn.recv(65535)

    conn.send("profile \"CiscoTAC-1\"\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("no active\n")
    time.sleep(2)
    output = conn.recv(65535)

    conn.send("profile \"CiscoSatelliteHTTP\"\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("reporting smart-licensing-data\n")
    time.sleep(2)
    output = conn.recv(65535)

    conn.send("destination transport-method http\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("no destination transport-method email\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("destination address http http://" + SatIP + ":" + SatPort + "/Transportgateway/services/DeviceRequestHandler\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("active\n")
    time.sleep(2)
    output = conn.recv(65535)
    
    conn.send("end\n")
    time.sleep(2)
    output = conn.recv(65535)

def Register (conn, token):

    '''
    INPUT
        conn - Connection Handle that will be used to login the switch
        token - registration token that will be used once the query reaches the satellite.

    OUTPUT
        None
    '''
    
    conn.send("lic sm reg id " + token + " \n")
    time.sleep(2)
    auth_status = conn.recv(65535)


def main():
    """Main method that retrieves the devices"""

    # Calculate Execution Time - Start
    now = datetime.datetime.now()
    print("Current date and time when script starts: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Connect to Switch
    conn_pre = paramiko.SSHClient()
    conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn_pre.connect(HOST_SW, 22, USER_SW, PASS_SW)
    conn = conn_pre.invoke_shell()
    
    conn.send("term len 0 \n")
    time.sleep(.5)
    output = conn.recv(65535)
    
    Config_Profile(conn, SatIP, SatPort)
    Register(conn, token)
    
    conn.send("show license summary \n")
    time.sleep(1)
    output = conn.recv(65535)
    print(output)
    
    # Calculate Execution Time - End
    now = datetime.datetime.now()
    print("Current date and time when script finished: " + now.strftime("%Y-%m-%d %H:%M:%S"))
    
    conn.close()


if __name__ == '__main__':
    sys.exit(main())
