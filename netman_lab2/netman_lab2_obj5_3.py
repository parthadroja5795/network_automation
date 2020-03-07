#script to fetch different metrics from EC2 instances

#!/usr/bin/env python

import boto3
import datetime

if __name__ == "__main__":
    
    try:
        inst=[]
        j=0
        
        #specifying the instance type
        ec2=boto3.resource('ec2')
        
        #printing all running instances
        for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
            inst.append(status['InstanceId'])
        
        print("Total {} running instances detected. Which instance you want data for?".format(len(inst)))
        for i in inst:
            print("press",j+1,"for",inst[j])
            j=j+1
        try:
            integer=int(input())
            if 0 < integer <= len(inst):
                instance_id=inst[integer-1]
                print("Instance ID:",instance_id)
                
                #connecting to the AWS CloudWatch
                client = boto3.client('cloudwatch',region_name='us-west-1',aws_access_key_id="AWS account access key",aws_secret_access_key="AWS account secret key")
            
                #getting the metrics about EC2 instance
                response = client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='StatusCheckFailed',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instance_id,
                    },
                ],
                StartTime=datetime.datetime(2019, 2, 2),
                EndTime=datetime.datetime(2019, 3, 2),
                Period=86400,
                Statistics=[
                    'Average',
                ],
                Unit='Count'
                )
    
                for status_check in response['Datapoints']:
                    if 'Average' in status_check:
                        if(status_check['Average']==0):
                            print("Status Check: Passed")
                        else:
                            print("Status Check: Failed")
            
                response = client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instance_id,
                    },
                ],
                StartTime=datetime.datetime(2019, 2, 2),
                EndTime=datetime.datetime(2019, 3, 2),
                Period=86400,
                Statistics=[
                    'Average',
                ],
                Unit='Percent'
                )
    
                for cpu in response['Datapoints']:
                    if 'Average' in cpu:
                        print("CPUUtilization (Average):",cpu['Average'])
                
                response = client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkIn',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instance_id,
                    },
                ],
                StartTime=datetime.datetime(2019, 2, 2),
                EndTime=datetime.datetime(2019, 3, 2),
                Period=86400,
                Statistics=[
                    'Average',
                ],
                Unit='Bytes'
                )
    
                for nw_in in response['Datapoints']:
                    if 'Average' in nw_in:
                        print("NetworkIn (Average):",nw_in['Average'])
                
                response = client.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkOut',
                Dimensions=[
                    {
                    'Name': 'InstanceId',
                    'Value': instance_id,
                    },
                ],
                StartTime=datetime.datetime(2019, 2, 2),
                EndTime=datetime.datetime(2019, 3, 2),
                Period=86400,
                Statistics=[
                    'Average',
                ],
                Unit='Bytes'
                )
    
                for nw_out in response['Datapoints']:
                    if 'Average' in nw_out:
                        print("NetworkOut (Average):",nw_out['Average'])
            else:
                print("Only {} instances are there. Please try again with proper input.".format(len(inst)))
        except:
            print("Invalid instance choice selected. Please try again.")
    except:
        print("Please check Internet connection.")