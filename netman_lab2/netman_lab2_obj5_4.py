#script to monitor utilization of EC2 instances and spin extra resources automatically as needed

#!/usr/bin/env python

import boto3
import time
import smtplib

if __name__ == "__main__":

    try:
        while(1):
            inst=[]
            inst2=[]
            fault=[]
            j=0
            st=[]
            alarm_st=[]
            
            #specifying the instance type
            ec2=boto3.resource('ec2')
            for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
                inst.append(status['InstanceId'])
            
            print("Total {} running instances detected.".format(len(inst)))
            
            #connecting to the AWS CloudWatch
            client = boto3.client('cloudwatch',region_name='us-west-1',aws_access_key_id="AWS account access key",aws_secret_access_key="AWS account secret key")
            
            for i in inst:
                client.put_metric_alarm(
                    AlarmName='High_CPU_Utilization'+str(j),
                    ComparisonOperator='GreaterThanThreshold',
                    EvaluationPeriods=1,
                    MetricName='CPUUtilization',
                    Namespace='AWS/EC2',
                    Period=60,
                    Statistic='Average',
                    Threshold=0.2,
                    AlarmDescription='Alarm when server CPU exceeds 0.2%',
                    ActionsEnabled=True,
                    Dimensions=[
                        {
                          'Name': 'InstanceId',
                          'Value': i
                        },
                    ],
                    InsufficientDataActions=['arn:aws:automate:us-west-1:ec2:stop'],            
                )
                j=j+1
                
            #putting sleep for 7 minutes to let the new instances spin up
            time.sleep(420)
            ec2=boto3.resource('ec2')
            for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
                inst2.append(status['InstanceId'])
            
            print("Total {} instances were running before operations.".format(len(inst)))
            print("Total {} instances are running after operations.".format(len(inst2)))
            print("We need to spin up {} more instances.".format(len(inst)-len(inst2)))
            
            #finding instances that had higher utilization
            fault=list(set(inst) - set(inst2))
            
            #sending notification about the higher utilization
            fromaddr="sender email address"
            toaddrs="receiver email address"
            
            server=smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            username="sender email address"
            password="sender email password"
            server.login(username,password)
            
            for i in fault:
                msg="Instance {} had Low Utilization alarm so it is stopped and new resource is spun automatically. Please check.".format(i)
                server.sendmail(fromaddr,toaddrs,msg)
            print("Mail has been sent regarding the fault details.")
            server.quit()
            
            ec2.create_instances(ImageId='ami-0ad16744583f21877', MinCount=1, MaxCount=(len(inst)-len(inst2)))
            #putting sleep for 10 minutes means next iteration of utilization check will be run after 10 minutes
            time.sleep(6000)
    except:
        print("Please check Internet connection.")