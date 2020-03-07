#script to automate the DHCP configuration

#!/usr/bin/env python

from netmiko import ConnectHandler
import threading

if __name__ == "__main__":

    commands=['int fa 0/0','ip addr dhcp','no shu']
    t=[]
    
    def config(x):
        #SSH into router and run the required commands
        net_connect=ConnectHandler(**x)
        output=net_connect.send_config_set(commands)
    
    if __name__=="__main__":
    
        ios_r2={
        'device_type':'cisco_ios',
        'username':'lab',
        'password':'lab123',
        'ip':'198.51.100.20',
        }
        ios_r3={
        'device_type':'cisco_ios',
        'username':'lab',
        'password':'lab123',
        'ip':'198.51.100.30',
        }
        ios_r4={
        'device_type':'cisco_ios',
        'username':'lab',
        'password':'lab123',
        'ip':'198.51.100.40',
        }
        routers=[ios_r2,ios_r3,ios_r4]
        
        #starting each thread and passing the router details to thread
        for i in range(0,len(routers)):
            thread=threading.Thread(target=config,args=(routers[i],))
            thread.start()
            t.append(thread)
        
        #joining all threads
        for i in t:
            i.join()