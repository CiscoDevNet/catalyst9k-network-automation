#! /usr/bin/env python

from ncclient import manager

# use the IP address or hostname of your Cat9300
HOST = '172.26.211.124'

# use your user credentials to access the Cat9300
USER = 'cisco'
PASS = 'C1sc0dna'

# NETCONF Config Template to use
netconf_payload = open("grpc.xml").read()

if __name__ == '__main__':
    print("Configuration Payload:")
    print("----------------------")
    print(netconf_payload)

    with manager.connect(host=HOST, port=830,
                         username=USER,
                         password=PASS,
                         hostkey_verify=False) as m:

        # Send NETCONF <edit-config>
        netconf_reply = m.edit_config(netconf_payload, target="running")

        # Print the NETCONF Reply
        print(netconf_reply)
