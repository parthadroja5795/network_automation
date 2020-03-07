#script to configure cisco IOS-XR using NETCONF

#!/usr/bin/env python

from ncclient import manager

if __name__ == "__main__":
    
    #YANG template to configure hostname
    config1='''
    <config>
    <host-names xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg">
    <host-name> netman_lab9_XR </host-name>
    </host-names>
    </config>
    '''
    
    #YANG template to configure access-list
    config2='''
    <config>
    <ipv4-acl-and-prefix-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-acl-cfg">
    <accesses>
    <access>
    <access-list-name>Parth</access-list-name>
    <access-list-entries>
    <access-list-entry>
    <sequence-number>100</sequence-number>
    <grant>permit</grant>
    <source-network>
    <source-address>198.51.100.2</source-address>
    <source-wild-card-bits>0.0.0.0</source-wild-card-bits>
    </source-network>
    </access-list-entry>
    </access-list-entries>
    </acess>
    </acesses>
    </ipv4-acl-and-prefix-list>
    </config>
    '''
    
    #YANG template to configure loopback interface
    config3='''
    <config>
    <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <interface>
    <name> Loopback1 </name>
    <enabled>true</enabled>
    <ipv4>
    <address>
    <ip>10.11.12.13</ip>
    <netmask>255.255.255.255</netmask>
    </address>
    </ipv4>
    </interface>
    </interfaces>
    </config>
    '''
    
    #opening the NETCONF connection
    conn=manager.connect(host="198.51.100.10",port=22,username="netman",password="netman",hostkey_verify=False,device_params={'name':'iosxr'},allow_agent=False,look_for_keys=True)
    
    #pushing the configuration
    result1=conn.edit_config(config=config1)
    print("Configuration of Hostname completed.")
    result2=conn.edit_config(config=config2)
    print("Configuration of Access-List completed.")
    result3=conn.edit_config(config=config3)
    print("Configuration of Loopback Interface Completed.")
    
    #commiting the configuration
    conn.commit()