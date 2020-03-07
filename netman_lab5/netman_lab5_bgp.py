#script to automate the BGP configuration

#!/usr/bin/env python

import json
import os
from netmiko import ConnectHandler
import threading
import re
import time
from prettytable import PrettyTable

#declaring some global variables
global commands, R1, R2, stats
commands={}
R1={}
R2={}
stats={}

#function to save router config in text file
def write_config(i,data):
	file_name="netman_lab5_config_"+i+".txt"
	a=open(file_name,'w')
	a.write(data)
	a.close()
	print("Running configuration for {} is saved in {}".format(i,file_name))

#function to get the config for appropriate router from the bgp.json file
def generate_config(i):
	file_name2="netman_lab5_config_bgp.json"
	if os.path.isfile(file_name2):
		a=open(file_name2)
		data=json.load(a)
		a.close()

		#making a list that will contain all the commands
		commands=[]
		c2="router ospf "+str(data[i]["LocalAs_number"])
		commands.append(c2)
		for j in list(data[i]["NetworkListToAdvertise"]):
			c3="network "+j+" area "+str(data[i]["LocalAs_number"])
			commands.append(c3)
		c4="exit"
		commands.append(c4)
		c5="router bgp "+str(data[i]["LocalAs_number"])
		commands.append(c5)
		for j in list(data[i]["NeighborIP"].keys()):
			c6="neighbor "+data[i]["NeighborIP"][j]+" remote-as "+str(data[i]["NeighborRemoteAS"])
			commands.append(c6)
			if str(j)=="3":
				pass
			else:
				c7="neighbor "+data[i]["NeighborIP"][j]+" update-source loopback "+str(j)
				commands.append(c7)
		c8="exit"
		commands.append(c8)
		c9="exit"
		commands.append(c9)
		return commands
	else:
		print("{} doesn't exist.".format(file_name2))
		exit()

#function to deploy the config and getting the running config
def deploy_config(i,x):

	#get the required config
	commands[i]=generate_config(i)
	y=x[i]
	try:
		#connect to the router
		net_connect=ConnectHandler(**y)
	except:
		print("Check SSH configuration on router {}.".format(i))
	
	#pushing the config
	output=net_connect.send_config_set(commands[i])
	
	#handling any error in the config commands
	if "% Invalid" in str(output):
		print(output)
		print("Wrong command entered on CLI of {}. Please try again.".format(i))
		exit()
	else:
		print("Configuration successful on {}".format(i))
	
	#getting the running configuration
	output2=net_connect.send_command('sh run')
	
	#saving the configuration in a file
	write_config(str(i),output2)

	#terminating the SSH connection
	net_connect.disconnect()

#function to get the bgp summary
def get_bgp(i,x):
	try:
		#opening the SSH connection
		net_connect=ConnectHandler(**x)
	except:
		print("Check SSH configuration on router {}.".format(x))

	#getting the BGP details and parsing the output	
	output=net_connect.send_command('sh ip bgp neigh')
	reg_neighbor="(?<=BGP neighbor is )(\w*.\w*.\w*.\w*)"
	reg_remoteAS="(?<=remote AS )(\w*)"
	reg_state="(?<=BGP state = )(\w*)"
	
	match1=re.findall(reg_neighbor,output)
	match2=re.findall(reg_remoteAS,output)
	match3=re.findall(reg_state,output)
	if str(i)=="R1":
		R1["BGP Neighbor IP"]=match1
		R1["BGP Neighbor AS"]=match2
		R1["BGP Neighbor State"]=match3
	elif str(i)=="R2":
		R2["BGP Neighbor IP"]=match1
		R2["BGP Neighbor AS"]=match2
		R2["BGP Neighbor State"]=match3
	stats[str(i)]=R1
	stats[str(i)]=R2

def main():
	
	file_name1="netman_lab5_sshInfo.json"
	if os.path.isfile(file_name1):
		x=open(file_name1)
		ssh_conf=json.load(x)
		x.close()
	else:
		print("{} doesn't exist.".format(file_name1))

	t=[]
	#threads for parallel configuration
	for i in list(ssh_conf.keys()):
		thread=threading.Thread(target=deploy_config,args=(i,ssh_conf))
		thread.start()
		t.append(thread)

	#joining all threads
	for i in t:
		i.join()

	time.sleep(90)

	#threads for getting bgp summary
	t_get=[]
	for i in list(ssh_conf.keys()):
		thread=threading.Thread(target=get_bgp,args=(i,ssh_conf[i]))
		thread.start()
		t_get.append(thread)

	#joining all threads
	for i in t_get:
		i.join()

	#printing the bgp summary in table
	table_r1=PrettyTable(["BGP Neighbor IP","BGP Neighbor AS","BGP Neighbor State"])
	table_r2=PrettyTable(["BGP Neighbor IP","BGP Neighbor AS","BGP Neighbor State"])
	for i in list(stats.keys()):
		if i=="R1":
			for j in range(0,len(list(stats[i]["BGP Neighbor IP"]))):
				table_r1.add_row((stats[i]["BGP Neighbor IP"][j],stats[i]["BGP Neighbor AS"][j],stats[i]["BGP Neighbor State"][j]))
		elif i=="R2":
			for j in range(0,len(list(stats[i]["BGP Neighbor IP"]))):
				table_r2.add_row((stats[i]["BGP Neighbor IP"][j],stats[i]["BGP Neighbor AS"][j],stats[i]["BGP Neighbor State"][j]))

	print(table_r1)
	print(table_r2)