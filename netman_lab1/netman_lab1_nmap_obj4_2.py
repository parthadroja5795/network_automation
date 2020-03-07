#script to analyze different host IP files and find old/new devices in the home network

#!/usr/bin/env python

import re

if __name__ == "__main__":

    #reading the old host IPs file
    a=open("netman_lab1_nmap_obj4_1_hosts.txt")
    b=a.read()
    reg='\d+\.\d+\.\d+\.\d+'
    c=re.findall(reg,b)
    print("Devices connected to my home network",c)
    
    #reading the new host IPs file
    d=open("netman_lab1_nmap_obj4_2_hosts.txt")
    e=d.read()
    f=re.findall(reg,e)
    print("After 10 mins\nDevice connected to my home network",f)
    
    #getting the old/new hosts
    x=set(c)-set(f)
    y=set(f)-set(c)
    
    print("Newly connected devices to my home network",list(y))
    print("Devices which got disconnected from my home network",list(x))