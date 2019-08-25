# NBAR2 on Catalyst9k
Providing easy configuration  of NBAR2 on the Catalyst 9K.

# requirements
-- ncclient

-- IOS-XE running >/= 16.11.1 also enabled for NETCONF`

### Sample Run:
```
(py) bash-4.1$ python nbar.py  --host x.x.x.x -u cisco -p xyz -i GigabitEthernet1/0/23
Checking if switch is configured with advantage license
 switch is configured with advantage license procedding with interface config
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:90aaac74-56a3-4451-b5e4-ae06e5a51270" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>

 interface config successful, enabling http SERVICES
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:c40a340e-1579-4315-b125-ff86ca25ac38" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <ok/>
</rpc-reply>

NBAR configured successfully

```
