#driver script for netman lab4

#!/usr/bin/env python

import netman_lab4_tcpdump, netman_lab4_snmp, netman_lab4_aws

if __name__ == "__main__":
    
    #finding the MAC addresses from IPv6 tcpdump
    netman_lab4_tcpdump.get_mac_address("netman_lab4_tcpdump.pcap")
    
    #building NSOT by sending different SNMP requests
    netman_lab4_snmp.create_nsot()
    
    #plotting the CPU utilization graph
    netman_lab4_snmp.cpu_utilization_graph()
    
    #backing up configuration/monitoring files on AWS S3 bucket
    netman_lab4_aws.aws_backup()