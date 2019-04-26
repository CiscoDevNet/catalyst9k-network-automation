import sys
from argparse import ArgumentParser
import re
from xml.etree.ElementTree import XML
import xml.dom.minidom
from ncclient import manager 



def start_maintenance(netconf_connection, device_name):
  '''
  This procedure verifies if the successor Device name is present or not. 
  Return True if condition satisfied, else return False
  '''
  netconf_payload = '''
  <filter>
    <cdp-neighbor-details xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper">
      <cdp-neighbor-detail>
       </device-name>
      </cdp-neighbor-detail>
    </cdp-neighbor-details>
  </filter>
  '''
  netconf_reply = xml.dom.minidom.parseString(str(netconf_connection.get(netconf_payload)))
  print(netconf_reply.toprettyxml( indent = "  " ))
  return_val = False
 
  
  #Parse netconf_reply to see if hostname exists 
  
  oper_data = XML(netconf_reply.toxml("utf-8"))

  for data in oper_data.findall('{urn:ietf:params:xml:ns:netconf:base:1.0}data'):
    for element in data.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper}cdp-neighbor-details'):
      for service in element.findall('{http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper}cdp-neighbor-detail'):
        hostname = service.find('{http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper}device-name').text
        if hostname.upper() == device_name.upper():
          return_val = True
          break 
  
  return return_val

if __name__ == '__main__':
  parser = ArgumentParser(description='Select options.')
  parser.add_argument('--host', type=str, required=True, help="The device IP or DN")
  parser.add_argument('-u', '--username', type=str, default='cisco', help="Go on, guess!")
  parser.add_argument('-p', '--password', type=str, default='cisco', help="Yep, this one too! ;-)")
  parser.add_argument('--port', type=int, default=830, help="Specify this if you want a non-default port")
  parser.add_argument('-s','--successor_name', type=str, required=True, help="Specify the successor name")
  args = parser.parse_args()
  m =  manager.connect(host=args.host,
                       port=args.port,
                       username=args.username,
                       password=args.password,
                       device_params={'name':"iosxe"})
  val = start_maintenance(m, args.successor_name)
  print(val)