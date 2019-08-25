# Streaming telemetry sessions using GRPC Dial-Out
Providing easy configuration and monitoring of streaming telemetry subscriptions on the Catalyst 9K.

### Sample Run:
```
(py) bash-4.1$ python mdtcfg.py --host x.x.x.x -u cisco -p C1sc0dna --sourceaddr x.x.x.x --subscriptiontype interface --reciever x.x.x.x
  <config>
    <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
      <mdt-subscription>
        <subscription-id>502</subscription-id>
        <base>
          <stream>yang-push</stream>
          <encoding>encode-kvgpb</encoding>
          <source-vrf>Mgmt-vrf</source-vrf>
          <source-address>x.x.x.x</source-address>
          <period>1000</period>
          <xpath>/if:interfaces-state/interface/statistics</xpath>
        </base>
      <mdt-receivers>
        <address>x.x.x.x</address>
        <port>57500</port>
        <protocol>grpc-tcp</protocol>
      </mdt-receivers>
    </mdt-subscription>
    </mdt-config-data>
  </config>
  
True
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:27b6c648-c626-4629-8b53-5777a61499e1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
      <mdt-subscriptions>
        <mdt-receivers>
          <address>x.x.x.x</address>
          <port>57500</port>
          <protocol>grpc-tcp</protocol>
          <state>rcvr-state-connected</state>
          <comments/>
          <profile/>
          <last-state-change-time>2019-08-25T01:02:42.363624+00:00</last-state-change-time>
        </mdt-receivers>
      </mdt-subscriptions>
      <mdt-subscriptions>
        <mdt-receivers>
          <address>x.x.x.x</address>
          <port>57500</port>
          <protocol>grpc-tcp</protocol>
          <state>rcvr-state-connecting</state>
          <comments/>
          <profile/>
          <last-state-change-time>2019-08-25T06:59:34.743356+00:00</last-state-change-time>
        </mdt-receivers>
      </mdt-subscriptions>
    </mdt-oper-data>
  </data>
</rpc-reply>

True
<?xml version="1.0" ?>
<rpc-reply message-id="urn:uuid:c7c2a926-557b-49fc-8220-10be60b287c7" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
  <data>
    <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
      <mdt-subscriptions>
        <subscription-id xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">502</subscription-id>
        <base>
          <stream>yang-push</stream>
          <encoding>encode-kvgpb</encoding>
          <source-vrf>Mgmt-vrf</source-vrf>
          <source-address>x.x.x.x</source-address>
          <period>1000</period>
          <xpath>/if:interfaces-state/interface/statistics</xpath>
        </base>
        <type>sub-type-static</type>
        <state>sub-state-valid</state>
        <comments/>
        <mdt-receivers>
          <address>x.x.x.x</address>
          <port>57500</port>
          <protocol>grpc-tcp</protocol>
          <state>rcvr-state-connecting</state>
          <comments/>
          <profile/>
          <last-state-change-time>2019-08-25T06:59:34.743356+00:00</last-state-change-time>
        </mdt-receivers>
        <last-state-change-time>2019-08-25T06:59:34.741049+00:00</last-state-change-time>
      </mdt-subscriptions>
    </mdt-oper-data>
  </data>
</rpc-reply>

subscription id is 502
True
```
