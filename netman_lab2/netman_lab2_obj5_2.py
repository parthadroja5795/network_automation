#script to automatically spin new EC2 instances in AWS and fetch information about them

#!/usr/bin/env python

import boto3
import time
from prettytable import PrettyTable

if __name__ == "__main__":

    try:
        a=[]
        iid=[]
        itype=[]
        ip=[]
        status=[]
        
        #specifying instance type and image type
        ec2=boto3.resource('ec2')
        ec2.create_instances(ImageId='ami-0ad16744583f21877', MinCount=1, MaxCount=2)
        time.sleep(60)
        
        #getting information about all running EC2 instances
        x=ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for i in x:
            a.append(i.id)
            ec2.instances.filter(InstanceIds=a).stop()
            break
        time.sleep(60)
        
        #getting information about all stopped EC2 instances
        y=ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running','stopped']}])
        for i in y:
            iid.append(i.id)
            itype.append(i.instance_type)
            status.append(i.state['Name'])
            ip.append(i.public_ip_address)
        
        #printing the information about the EC2 instances
        table=PrettyTable(["Instance ID","Instance Type","Instance IP","Instance Status"])
        for i in range(0,len(iid)):
            table.add_row((iid[i],itype[i],ip[i],status[i]))
        print(table)
        
    except:
        print("Check your Internet connection.")