#driver script for netman lab5

#!/usr/bin/env python

import netman_lab5_sshInfo, validateIP, connectivity, netman_lab5_bgp
import os
import json

if __name__ == "__main__":

	#generating JSON file containing all SSH login information 
	netman_lab5_sshInfo.generate_sshinfo()
	
	file_name="netman_lab5_sshInfo.json"
	
	ip=[]
	
	if os.path.isfile(file_name):
		a=open(file_name)
		b=json.load(a)
		for i in list(b.keys()):
			ip.append(b[i]["ip"])
	
	#checking validity for all SSH IP addresses
	for i in ip:
		validateIP.validateIP(i)
	
	#checking reachability for all SSH IP addresses
	for i in ip:
		connectivity.check_connectivity(i)
	
	#running the BGP automation script
	netman_lab5_bgp.main()