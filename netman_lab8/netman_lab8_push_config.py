#script to push the configuration to the routers

#!/usr/bin/env python

import os
from netmiko import ConnectHandler
import json
import threading

#function to push the config
def push_config(i,ssh_details,config_details):
	commands=[]
	if os.path.isfile(config_details):
		
		#opening the config file
		open_config=open(config_details)
		
		#making list of all config commands
		for line in open_config:
        		if line.strip():
                		commands.append(line.strip())

		#opening the SSH connection
		conn=ConnectHandler(**ssh_details)
		print("connected to {}".format(i))
		
		#pushing the config
		o1=conn.send_config_set(commands)
		print("configuration successful on {}".format(i))
		
		#closing the SSH connection
		conn.disconnect()

	else:
		print("{} doesn't exists. Please check".format(config_details))
		
		
if __name__=="__main__":

	#getting the SSH login information from json file
	filename="netman_lab8_sshInfo.json"
	a=open(filename)
	ssh_info=json.load(a)
	a.close()

	#loading all the router config file
	config_info={}
	config_info['R1']="netman_lab8_R1_config.txt"
	config_info['R2']="netman_lab8_R2_config.txt"
	config_info['R3']="netman_lab8_R3_config.txt"

	t=[]
	#starting the thread to push the config to the routers
	for i in list(config_info.keys()):
		thread=threading.Thread(target=push_config,args=(i,ssh_info[i],config_info[i]))
		thread.start()
		t.append(thread)

	#joining all the threads
	for i in t:
		i.join()