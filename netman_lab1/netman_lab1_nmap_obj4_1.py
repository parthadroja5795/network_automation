#script to scan the home network with nmap and get the host IPs

#!/usr/bin/env python

import subprocess
import re

if __name__ == "__main__":

    #running nmap over the network to find all connected hosts
    x=subprocess.Popen(['nmap','-sP','10.0.0.1-255'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    y=x.stdout.read()
    
    #parsing the nmap output to get the IP addresses
    reg='\d+\.\d+\.\d+\.\d+'
    match=re.findall(reg,y)
    
    #storing all host IPs in a file
    b=open("netman_lab1_nmap_obj4_1_hosts.txt","wb")
    b.write(str(match))
    b.close()