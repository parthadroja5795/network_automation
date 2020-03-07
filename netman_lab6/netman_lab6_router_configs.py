#script to generate JSON file containing all SSH login information

#!/usr/bin/env python

import json

if __name__ == "__main__":
	
	x={}
	y={}
	z={}
	w={}
	v={}
	
	x["username"]="netman"
	x["device_type"]="cisco_ios"
	x["ip"]="198.51.101.10"
	x["password"]="netman"
	
	y["username"]="netman"
	y["device_type"]="cisco_ios"
	y["ip"]="198.51.101.20"
	y["password"]="netman"
	
	v["username"]="netman"
	v["device_type"]="cisco_ios"
	v["ip"]="172.16.1.30"
	v["password"]="netman"
	
	w["username"]="netman"
	w["device_type"]="cisco_ios"
	w["ip"]="198.51.101.40"
	w["password"]="netman"
	
	z["R1_adroja"]=x
	z["R2_adroja"]=y
	z["R3_adroja"]=v
	z["R4_adroja"]=w
	
	filename="/home/netman/Lab6/netman_lab6_router_configs.json"
	a=open(filename,'w')
	json.dump(z,a)
	a.close()
	
	print("Router SSH configuration is saved in netman_lab6_router_configs.json file.")