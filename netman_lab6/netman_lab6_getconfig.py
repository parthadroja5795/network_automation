#script to get running configuration of all routers

#!/usr/bin/env python

import json
from napalm import get_network_driver
import threading
import time
import validateIP
import connectivity
import flask

files={}

#function to get the running configuration of router
def get_run_config(i,x):
	
	driver=get_network_driver('ios')
	
	#opening the SSH connection
	conn=driver(x["ip"],x["username"],x["password"])
	conn.open()
	
	#getting the running config
	o1=conn.get_config()
	
	#adding timestamp to the filename
	t=time.strftime("%Y-%m-%dT%H:%M:%SZ")
	file_name="".join(i)+"_ISO7200_"+t+".txt"
	
	#storing the running config in the file
	a=open(file_name,"w")
	a.write(str(o1["running"]))
	a.close()
	files[i]=file_name
	
	#closing the SSH connection
	conn.close()

def get_config(config_info):

	#validating the IP addresses present in the SSH info file
	for i in list(config_info.keys()):
		validateIP.validateIP(config_info[i]["ip"])

	#checking reachability to the IP addresses present in the SSH info file
	for i in list(config_info.keys()):
		connectivity.check_connectivity(config_info[i]["ip"])

	t=[]
	#starting the thread to get the running configuration
	for i in list(config_info.keys()):
		thread=threading.Thread(target=get_run_config,args=(i,config_info[i]))
		thread.start()
		t.append(thread)

	#joining all threads
	for i in t:
		i.join()
	
	#storing the config filenames in a separate file for future use
	file_name="netman_lab6_current_config.txt"
	z=open(file_name,'w')
	json.dump(files,z)
	z.close()
	return files