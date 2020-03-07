#script to monitor different network parameters and display in a dashboard as well as send automated notification in real-time for any detected fault 

#!/usr/bin/env python

import subprocess
import json
from easysnmp import Session,snmp_get,snmp_walk
from prettytable import PrettyTable
from twilio.rest import Client
import smtplib
import time
    
#function to send automated text message using Twilio API
def send_twilio(x,y,tt):
	#SID and Token for authentication on Twilio API
	account_sid = "Twilio account SID"
	auth_token = "Twilio account authentication token"
	client = Client(account_sid, auth_token)
	
	#defining the text message
	message_info="This is an automated message from NOC. Interface {} is down on Router {}. IM{} is generated for the same. Please check.".format(y,x,tt)
	
	#sending the text message
	message = client.messages.create(
				body=message_info,
				from_="Twilio phone number",
				to="Receiver phone number"
				)

#function to send automated mail using SMTP
def send_smtp(x,y,tt):
	
	#logging into smtp server
	fromaddr="sender email address"
	toaddrs="receiver email address"
	server=smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	username="sender email address"
	password="sender email password"
	server.login(username,password)
	
	#defining the text message
	msg="This is an automated message from NOC. Interface {} is down on Router {}. IM{} is generated for the same. Please check.".format(y,x,tt)
	
	#sending the email
	server.sendmail(fromaddr,toaddrs,msg)
	server.quit()

if __name__ == "__main__":
	
	#loading the SSH login information from a file
	filename="netman_lab10_sshInfo.json"
	a=open(filename)
	b=json.load(a)
	parameters={}

	#periodically polling the network parameters for real-time monitoring
	while(1):
		for i in list(b.keys()):
			router={}
			try:
				
				#opening the SNMP session
				session=Session(hostname=b[i]['ip'],community="public",version=2)
			
				#sending SNMP request to get router uptime
				op1=session.get('1.3.6.1.2.1.1.3.0')
				z1=str(op1.value)
				uptime=z1[0:len(z1)-2]
				uptime2=int(int(uptime)/3600)
	
				#defining OIDs for different interfaces and their status
				int_name=["1.3.6.1.2.1.31.1.1.1.1.1","1.3.6.1.2.1.31.1.1.1.1.2","1.3.6.1.2.1.31.1.1.1.1.3","1.3.6.1.2.1.31.1.1.1.1.4","1.3.6.1.2.1.31.1.1.1.1.5"]
				int_status=["1.3.6.1.2.1.2.2.1.7.1","1.3.6.1.2.1.2.2.1.7.2","1.3.6.1.2.1.2.2.1.7.3","1.3.6.1.2.1.2.2.1.7.4","1.3.6.1.2.1.2.2.1.7.5"]
				status={}
				name={}
				
				#sending SNMP requsts to get interface status
				for j in range(0,5):
					op1=session.get(int_status[j])
					op2=session.get(int_name[j])
					if str(op1.value)!="1":
						status[j]="Down"
						file_name="netman_lab10_ttnumber.txt"
						a=open(file_name)
						tt=a.read()
						
						#calling notification functions if any interface is down
						send_twilio(i,str(op2.value),tt)
						send_smtp(i,str(op2.value),tt)
					else:
						status[j]="Up"
					name[j]=op2.value	
				
				#sending SNMP request to get router CPU utilization
				op3=session.get('1.3.6.1.4.1.9.2.1.56.0')
				
			except:
				uptime2="unknown"
				for j in range(0,5):
					status[j]="unknown"
					name[j]="unknown"
				status[4]="Down"
	
			#saving the polled information in a dictionary
			router["uptime"]=uptime2
			router["name"]=name
			router["status"]=status
			router["utilization"]=str(op3.value)
	
			parameters[i]=router
	
		#printing the polled parameters in a table format	
		table=PrettyTable(["Router","Uptime","Fa0/0","Fa0/1","Fa1/0","Fa1/1","Managment","CPU Utilization"])
	
		for i in list(b.keys()):
			table.add_row((i,str(parameters[i]["uptime"])+" hours",parameters[i]["status"][0],parameters[i]["status"][1],parameters[i]["status"][2],parameters[i]["status"][3],parameters[i]["status"][4],str(parameters[i]["utilization"])+"%"))
		print(table)
		time.sleep(5)