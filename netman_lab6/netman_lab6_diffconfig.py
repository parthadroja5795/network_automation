#script to find the difference between running configuration and old configuration

#!/usr/bin/env python

import json
from napalm import get_network_driver
import threading
import time
import sqlite3

diff={}

#function to find the difference between configurations of router
def get_diff_config(i,day0):

	#opening SSH connection
	driver=get_network_driver('ios')
	conn=driver(i[7],i[1],i[2])
	conn.open()
	print("Connected to {}".format(i[0]))
	
	#loading old configuration file
	conn.load_replace_candidate(filename=day0[i[0]])

	#comparing running and old configuration to find the difference
	diffs=conn.compare_config()
	if len(diffs)>0:
		diff[i[0]]=diffs
	else:
		print("No difference in the config file for {}".format(i))
		diff[i]="No Difference"
	
	#closing the SSH connection
	conn.close()

def get_diff(database):
	
	#loading the SSH information database
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	query3="select * from ospfconfig"
	cur.execute(query3)
	b3=cur.fetchall()
	cur.close()
	
	#loading the old configuration filename file
	file_name="netman_lab6_current_config.txt"
	z=open(file_name,'r')
	day0=json.load(z)

	#starting the thread to find the difference between configurations
	t=[]
	for i in b3:
		thread=threading.Thread(target=get_diff_config,args=(i,day0))
		thread.start()
		t.append(thread)
	
	#joining all threads
	for i in t:
		i.join()

	return diff