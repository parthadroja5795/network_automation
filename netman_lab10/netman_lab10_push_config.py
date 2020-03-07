#script to push the configuration to the routers

#!/usr/bin/env python

import os
from netmiko import ConnectHandler
import json
import threading

#function to load the configuration from the file and push to the routers 
def push_config(i,ssh_details,config_details):
	
	commands=[]
	
	if os.path.isfile(config_details):
		
		#loading the configuration from the file
		open_config=open(config_details)
		for line in open_config:
			if line.strip():
				commands.append(line.strip())
		
		#opening the SSH connection
		conn=ConnectHandler(**ssh_details)
		print("Connected to {} for configuration.".format(i))
		
		#pushing the configurations
		o1=conn.send_config_set(commands)
		
		#closing the SSH connection
		conn.disconnect()
		print("Configuration completed on {}.".format(i))
	else:
		print("{} doesn't exists. Please check.".format(config_details))

if __name__=="__main__":
 
	#loading the SSH login information from a file
	filename="netman_lab10_sshInfo.json"
	a=open(filename)
	ssh_info=json.load(a)
	a.close()
	
	#specifying the router configuration file names
	config_info={}
	config_info['Edge1']="netman_lab10_Edge-1_config.txt"
	config_info['Edge2']="netman_lab10_Edge-2_config.txt"
	config_info['Edge3']="netman_lab10_Edge-3_config.txt"
	config_info['Edge4']="netman_lab10_Edge-4_config.txt"
	config_info['Core1']="netman_lab10_Core-1_config.txt"
	config_info['Core2']="netman_lab10_Core-2_config.txt"
	
	t=[]
	#starting the threads to push the configuration tot he routers
	for i in list(config_info.keys()):
	        thread=threading.Thread(target=push_config,args=(i,ssh_info[i],config_info[i]))
	        thread.start()
	        t.append(thread)
	
	#joining all the threads
	for i in t:
	        i.join()