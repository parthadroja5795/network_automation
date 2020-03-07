#driver script for netman lab6

#!/usr/bin/env python

from flask import Flask,render_template,request
import os
import netman_lab6_getconfig
import netman_lab6_ospfconfig
import netman_lab6_diffconfig
import netman_lab6_migration
import time
import json
import sqlite3

#function to create the table in SQL database
def create_table(cur):
	cur.execute('CREATE TABLE IF NOT EXISTS ospfconfig(router TEXT, username TEXT, password TEXT, pid TEXT, aid TEXT, loopback TEXT, networks TEXT, ssh_ip TEXT)')

#function to add entry in SQL database table
def data_entry(h,a,b,c,d,e,f,g,cur,conn):
	cur.execute("INSERT INTO ospfconfig (router, username, password, pid, aid, loopback, networks, ssh_ip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(h,a,b,c,d,e,f,g))
	conn.commit()

#flask application
app=Flask(__name__)
@app.route('/')
def index():
	#displaying home page
	return render_template('netman_lab6_index.html')

#function to store the running configurations in files
@app.route('/first',methods = ['GET', 'POST'])
def first():
	a=open("lab6_router_configs.json","r")
	config_info=json.load(a)
	a.close()
	files=lab6_getconfig.get_config(config_info)
	return render_template('netman_lab6_page1.html',files=files)

#function to get user inputs from webpage
@app.route('/second',methods = ['GET', 'POST'])
def second():  
	return render_template('netman_lab6_page2.html')

#function to find the difference between the configurations
@app.route('/third',methods = ['GET', 'POST'])
def third():
	database="lab6_ospf.db"
	diff=lab6_diffconfig.get_diff(database)
	return render_template('netman_lab6_page3.html',diff=diff)

#function to perform the migration of the router
@app.route('/forth',methods= ['GET', 'POST'])
def forth():
	database="netman_lab6_ospf.db"
	
	#changing the OSPF interface cost
	r4=lab6_migration.change_ospf_cost(database)
	
	#checking the traffic via the router
	lab6_migration.check_utilization(r4)
	
	#shutting down the interface
	lab6_migration.shutdown_interface(r4)
	
	#bringing the router back into production
	a=lab6_migration.noshutdown_interface(r4)
	
	return render_template('netman_lab6_page4.html',a=a)

#function to read the user inputs from the webpage, configure OSPF and verify it
@app.route('/ospf', methods = ['GET', 'POST'])
def ospf():
	
	#reading the user inputs from the webpage
	a1=request.form['r1_username']
	b1=request.form['r1_password']
	c1=request.form['r1_ospf_process_id']
	d1=request.form['r1_ospf_area_id']
	e1=request.form['r1_ospf_loopback_ip']
	f1=request.form['r1_ospf_network']
	g1=request.form['r1_ssh_ip']

	a2=request.form['r2_username']
	b2=request.form['r2_password']
	c2=request.form['r2_ospf_process_id']
	d2=request.form['r2_ospf_area_id']
	e2=request.form['r2_ospf_loopback_ip']
	f2=request.form['r2_ospf_network']
	g2=request.form['r2_ssh_ip']

	a3=request.form['r3_username']
	b3=request.form['r3_password']
	c3=request.form['r3_ospf_process_id']
	d3=request.form['r3_ospf_area_id']
	e3=request.form['r3_ospf_loopback_ip']
	f3=request.form['r3_ospf_network']
	g3=request.form['r3_ssh_ip']

	a4=request.form['r4_username']
	b4=request.form['r4_password']
	c4=request.form['r4_ospf_process_id']
	d4=request.form['r4_ospf_area_id']
	e4=request.form['r4_ospf_loopback_ip']
	f4=request.form['r4_ospf_network']
	g4=request.form['r4_ssh_ip']

	h1="R1_adroja"
	h2="R2_adroja"
	h3="R3_adroja"
	h4="R4_adroja"

	database="lab6_ospf.db"
	
	try:
		os.remove(database)        
	except:
		pass

	#making database from the user inputs
	conn=sqlite3.connect(database)
	cur=conn.cursor()
	create_table(cur)
	data_entry(h1,a1,b1,c1,d1,e1,f1,g1,cur,conn)
	data_entry(h2,a2,b2,c2,d2,e2,f2,g2,cur,conn)
	data_entry(h3,a3,b3,c3,d3,e3,f3,g3,cur,conn)
	data_entry(h4,a4,b4,c4,d4,e4,f4,g4,cur,conn)
	cur.close()
	conn.close()

	#getting the interface IPs
	lab6_ospfconfig.get_interfaces(database)

	#configuring OSPF
	lab6_ospfconfig.config_ospf(database)
	time.sleep(30)
	
	#verifying the OSPF configuration
	ping=lab6_ospfconfig.ping_loopbacks(database)
	return render_template('netman_lab6_page2_1.html',data=ping)

#running the flask application
if __name__=='__main__':
	app.debug = True
	app.run(host='0.0.0.0',port=80)