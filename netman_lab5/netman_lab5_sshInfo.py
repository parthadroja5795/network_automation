#script to generate JSON file containing all SSH login information

#!/usr/bin/env python

import re
import os
import subprocess
import threading
import json

#function to generate the JSON file containing all SSH login information
def generate_sshinfo():

	r={}
	r1={}
	r2={}

	r1["username"]="netman"
	r1["password"]="netman"
	r1["ip"]="198.51.100.1"
	r1["device_type"]="cisco_ios"

	r2["username"]="netman"
	r2["password"]="netman"
	r2["ip"]="198.51.100.3"
	r2["device_type"]="cisco_ios"

	r["R1"]=r1
	r["R2"]=r2

	#saving the SSH login information in a file
	file_name=open("netman_lab5_sshInfo.json","w")
	json.dump(r,file_name)
	file_name.close()