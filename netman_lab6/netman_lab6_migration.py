#script to automate the migration of the router

#!/usr/bin/env python

import threading
from napalm import get_network_driver
import json
import re
import time
from netmiko import ConnectHandler
import sqlite3

r4={}

#function to change the OSPF cost on the router
def change_ospf_cost(database):

	#getting the SSH information from the database
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	t=("R4_adroja",)
	query4="select * from ospfconfig where router=?"
	cur.execute(query4,t)
	b4=cur.fetchall()
	cur.close()

	r4["ip"]=b4[0][7]
	r4["username"]=b4[0][1]
	r4["password"]=b4[0][2]
	r4["device_type"]="cisco_ios"

	#opening SSH connection
	driver=get_network_driver('ios')
	conn=driver(r4["ip"],r4["username"],r4["password"])
	conn.open()
	print("Connected to R4 for migration.")
	
	#changing the OSPF cost on the router
	conn.load_merge_candidate(filename="netman_lab6_migration_1.cfg")
	print("Changing the OSPF cost of interfaces on R4.")
	diffs=conn.compare_config()
	if len(diffs)>0:
		try:
			conn.commit_config()
		except IOError:
			pass
	else:
		print("No cost changes needed.")

	#closing the SSH connection
	conn.close()
	return r4

#function to shutdown the interfaces on the router
def shutdown_interface(r4):

	#opening SSH connection
	driver=get_network_driver('ios')
	conn=driver(r4["ip"],r4["username"],r4["password"])
	conn.open()
	
	#shutting down the interfaces on the router
	conn.load_merge_candidate(filename="netman_lab6_migration_2.cfg")
	print("Shutting down R4 and putting the banner.")
	diffs=conn.compare_config()
	if len(diffs)>0:
		try:
			conn.commit_config()
		except IOError:
			pass
	else:
		print("No interface changes needed.")

	#closing the SSH connection
	conn.close()
	print("R4 is out of production now.")

#function to "no shutdown" the interfaces on the router
def noshutdown_interface(r4):

	#opening the SSH connection
	driver=get_network_driver('ios')
	conn=driver(r4["ip"],r4["username"],r4["password"])
	conn.open()
	print("Bringing R4 back into production.")

	#changing the interfaces status to "no shutdown" on the router
	conn.load_merge_candidate(filename="netman_lab6_migration_3.cfg")
	diffs=conn.compare_config()
	if len(diffs)>0:
		try:
			conn.commit_config()
		except IOError:
			pass
	else:
		print("No interface changes needed.")	

	print("Migration Successful.")
	
	#closing the SSH connection
	conn.close()
	return "Migration completed successfully."	

#function to check the link utilization after changing the OSPF cost on the router
def check_utilization(r4):

	#opening the SSH connection
	conn=ConnectHandler(**r4)
	print("Connected to R4 to check the current traffic.")

	#getting the current input and output rate on the router interface
	o1=conn.send_command("sh int fa 0/0 | i rate")
	reg="(?<=rate )(\w*)"
	rate=re.findall(reg,str(o1))

	#proceeding with migration only if there is no traffic via the router
	if rate[0]=="0" and rate[1]=="0":
		print("There is no traffic on R4. Good for migration now.")
	else:
		print("There is traffic on R4. Waiting for traffic to re-route and checking utilization again after sometime.")
		time.sleep(60)
		check_utilization(r4)