#script to automate the OSPF configuration via user friendly webpage

#!/usr/bin/env python

from flask import Flask,render_template,request
import os
import json
import validateIP
import connectivity
import threading
from napalm import get_network_driver
from prettytable import PrettyTable
import subprocess
from netmiko import ConnectHandler
import sqlite3

ip_info={}
loopback=[]
ping={}
r1={}

#function to check the OSPF configuration
def ping_loopbacks(database):
	
	#getting SSH information from database
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	t=("R1_adroja",)
	query4="select * from ospfconfig where router=?"
	cur.execute(query4,t)
	b4=cur.fetchall()
	cur.close()

	r1["ip"]=b4[0][7]
	r1["username"]=b4[0][1]
	r1["password"]=b4[0][2]
	r1["device_type"]="cisco_ios"

	#opening the SSH connection
	connect=ConnectHandler(**r1)

	#getting the loopback IPs
	cur=conn.cursor()
	query5="select router,loopback from ospfconfig"
	cur.execute(query5)
	b5=cur.fetchall()
	cur.close()

	#pinging all the loopback IPs	
	for i in b5:
		ip=i[1]
		o1=connect.send_command('ping '+str(ip))
		ping[i[0]]=o1
	return ping

	#closing the SSH connection
	connect.disconnect()

#function to push the OSPF config
def push_config(a,b,c,d,e,f,g,h):

	#opening the SSH connection
	driver=get_network_driver('ios')
	conn=driver(h,b,c)
	conn.open()
	print("Connected to {} for configuration".format(a))

	#loading the OSPF config file
	conn.load_merge_candidate(filename=a+"_ospf_config.cfg")

	#pushing the OSPF config
	diffs=conn.compare_config()
	if len(diffs)>0:
		try:
			conn.commit_config()
		except IOError:
			pass
	else:
		print("No changes needed on {}".format(a))

	print("Finished configuring {}".format(a))
	conn.close()

#function to generate OSPF config file
def config_ospf(database):
	
	#getting config parameters form the database
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	query3="select * from ospfconfig"
	cur.execute(query3)
	b3=cur.fetchall()
	cur.close()
	
	#generating the OSPF config file
	for i in b3:
		file_name="".join(i[0]+"_ospf_config.cfg")
		try:
			os.remove(file_name)
		except:
			pass

		z=open(file_name,'a')
		a="router ospf "+i[3]+"\n"
		z.write(a)

		b=" log-adjacency-changes\n"
		z.write(b)
		c=" network "+i[5]+" 0.0.0.0 "+"area "+i[4]+"\n"
		z.write(c)

		p=i[6]
		q=p.split(",")
		for r in q:
			s=r.split(":")
			d=" network "+s[0]+" 0.0.0.255 "+"area "+s[1]+"\n"
			z.write(d)
		z.close()

	t=[]

	#starting threads to push the OSPF config
	for i in b3:
		thread=threading.Thread(target=push_config,args=(i))
		thread.start()
		t.append(thread)

	#joining all threads
	for i in t:
		i.join()

#function to get interfaces IP
def ip_interfaces(a,b,c,d,e,f,g,h):

	#opening SSH connection
	driver=get_network_driver('ios')
	conn=driver(h,b,c)
	conn.open()
	
	#getting interface IPs
	o1=conn.get_interfaces_ip()

	#closing the connection
	conn.close()
	ip_info[a]=o1

#function to print the interfaces IP
def get_interfaces(database):

	#getting loopback IPs from the database
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	query1="select loopback from ospfconfig"
	cur.execute(query1)
	b1=cur.fetchall()
	cur.close()

	#validating the loopback IPs
	for i in b1:
		validateIP.validateIP(i[0])

	#getting SSH IPs from the database
	cur=conn.cursor()
	query2="select ssh_ip from ospfconfig"
	cur.execute(query2)
	b2=cur.fetchall()
	cur.close()

	#validating and checking reachability to the SSH IPs
	for i in b2:
		validateIP.validateIP(i[0])
		connectivity.check_connectivity(i[0])

	#getting SSH information from the database
	cur=conn.cursor()
	query3="select * from ospfconfig"
	cur.execute(query3)
	b3=cur.fetchall()
	cur.close()

	t=[]
	
	#starting threads to get interface IPs	
	for i in b3:
		thread=threading.Thread(target=ip_interfaces,args=(i))
		thread.start()
		t.append(thread)

	#joining all threads
	for i in t:
		i.join()

	loopback=[]
	
	#printing all the interface IPs
	table=PrettyTable(["Router Hostname","Interface IPs"])
	for i in list(ip_info.keys()):
		li=[]
		for j in list(ip_info[i].keys()):
			if j=="Loopback1":
				w=list((ip_info[i][j]["ipv4"].keys()))[0]
				loopback.append(w)
			y=ip_info[i][j]
			z=ip_info[i][j]["ipv4"][list(ip_info[i][j]["ipv4"].keys())[0]]["prefix_length"]
			x=list(ip_info[i][j]["ipv4"].keys())[0]

			st=j+":"+x+"/"+str(z)
			li.append(str(st))
		table.add_row((i,li))

	print(table)

	#checking whether the loopback IPs are configured on routers or not
	for i in b1:
		x=i[0]
		if x in loopback:
			print("{} is present on the network".format(x))