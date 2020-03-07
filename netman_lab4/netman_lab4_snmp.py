#script to build NSOT by sending different SNMP requests

#!/usr/bin/env python

from easysnmp import Session,snmp_get,snmp_walk
import subprocess
import json
import time
import matplotlib.pyplot as p

def create_nsot():
    routers={'R1':'20.0.0.1','R2':'10.0.0.2','R3':'10.0.0.3','R4':'198.51.100.40','R5':'10.0.0.1'}
    
    final={}
    final_status={}
    
    for r in list(routers.keys()):
        ipv4={}
        ipv6={}
        test_address={}
        interface={}
        add={}
        status={}
        test_status={}
        ip=routers[r]
        
        #opening SNMP session with the router
        session=Session(hostname=ip,community='public',version=2)
        
        #sending SNMP requests
        op1 = session.walk('ifName')
        op2 = session.walk('ipAdEntIfIndex')
        x1=subprocess.Popen(['snmpbulkwalk','-v','2c','-c','public',ip,'ipAddressIfIndex.ipv6'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        y2=x1.stdout.read().strip()
        op3 = session.walk('ifOperStatus')
            
        #getting the interface status
        for i in op3:
            if i.oid_index=='1':
                if str(i.value)=='1':
                    status[1]="Up"
                else:
                    status[1]="Down"
            elif i.oid_index=='2':
                if str(i.value)=='1':
                    status[2]="Up"
                else:
                    status[2]="Down"
            elif i.oid_index=='3':
                if str(i.value)=='1':
                    status[3]="Up"
                else:
                    status[3]="Down"
            
        z2=y2.split("\n")
    
        #getting the ipv6 address
        for i in z2:
            if(i[91]=='1'):
                ipv6[1]=i[31:78]   
            elif(i[91]=='2'):
                ipv6[2]=i[31:78]
            elif(i[91]=='3'):
                ipv6[3]=i[31:78]
        
        #getting the interface name
        for i in op1:
            if i.oid_index=='1':
                interface[1]=str(i.value)
            elif i.oid_index=='2':
                interface[2]=str(i.value)
            elif i.oid_index=='3':
                interface[3]=str(i.value)
        
        #getting the ipv4 address
        for i in op2:
            if str(i.value)=='1':
                ipv4[1]=str(i.oid_index)
            elif str(i.value)=='2':
                ipv4[2]=str(i.oid_index)
            elif str(i.value)=='3':
                ipv4[3]=str(i.oid_index)
    
        #building the NSOT
        for i in list(interface.keys()):
            test={}
            try:
                test['v4']=ipv4[i]
            except:
                test['v4']="Null"
            try:
                test['v6']=ipv6[i]
            except:
                test['v6']="Null"
            
            test_address[interface[i]]=test
            
        add["addresses"]=test_address
    
        for i in list(interface.keys()):
            status_test={}
            test_status[interface[i]]=status[i]
    
        final_status[r]=test_status
        final[r]=add
    print("IP addresses of all interfaces on all routers")
    print(final)
    print("Admin status of all interfaces on all routers")
    print(final_status)
    
    #saving the information in a file
    file_name=open("netman_lab4_snmp.txt",'a')
    json.dump(final,file_name)
    json.dump(final_status,file_name)
    
#function to plot the utilization graph
def cpu_utilization_graph():    
    ip="20.0.0.1"
    
    #opening the SNMP session
    session=Session(hostname=ip,community='public',version=2)
    utilization=[]
    
    #monitoring utilization every 5 second
    for i in range(0,25):
        op1 = session.get('.1.3.6.1.4.1.9.2.1.56.0')
        utilization.append(op1.value)
        time.sleep(5)
    
    #plotting the graph
    p.plot(utilization)
    p.xlabel("timestamp Number (Each interval is 5 sec)")
    p.ylabel("CPU Utilization (%)")
    p.title("CPU Utilization Graph")
    p.savefig('netman_lab4_utilization_graph.png')