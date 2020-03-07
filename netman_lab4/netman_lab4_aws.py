#script for automated backup of configuration/monitoring files on AWS S3 bucket

#!/usr/bin/env python

import subprocess
import boto3
import urllib3
from time import strftime
import boto
import time
from prettytable import PrettyTable
import datetime

urllib3.disable_warnings()

def aws_backup():
    
    #getting current time
    a=strftime("%Y_%m_%d_%H_%M_%S")
    
    #attaching the timestamp to the filename
    filename1="netman_lab4_aws_json_"+a+".txt"
    filename2="netman_lab4_utilization_graph_"+a+".png"
    
    try:
        #connecting to AWS S3
        s3 = boto3.resource('s3')
        
        #creating an AWS S3 bucket
        try:
            s3.create_bucket(Bucket='netman-lab4-parth', CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
        except:
            print("Bucket already exists")
        
        buck="netman-lab4-parth"
        
        #uploading files to the AWS S3 bucket
        try:
            s3.Bucket(buck).upload_file("/home/netman/netman_lab4_aws_json.txt", filename1)
            s3.Bucket(buck).upload_file("/home/netman/netman_lab4_utilization_graph.png", filename2)
        except:
            print("Please check the file names")
        
        filelist={}
        
        #printing all the filenames present on the AWS S3 bucket
        print("File content in {} bucket".format(buck))
        table=PrettyTable(["Filename","Last Modified (GMT)"])
        s32 = boto.connect_s3()
        bucket = s32.lookup(buck)
        for key in bucket:
            string=str(key.last_modified)
            filelist[key.name]=string
            table.add_row((str(key.name),string))
        print(table)

        #checking the last modified time of all the files
        for z in list(filelist.keys()):
            b=filelist[z]
            c=b[0:4]+"_"+b[5:7]+"_"+b[8:10]+"_"+b[11:13]+"_"+b[14:16]+"_"+b[17:19]
            
            format_time='%Y_%m_%d_%H_%M_%S'
            tdelta=datetime.datetime.strptime(c,format_time)-datetime.datetime.strptime(a,format_time)
            print("Number of seconds since the file {} was last modified {}".format(str(z),int(tdelta.seconds)-25200))
            
            #deleting the file if its not modified in 5 minutes = 300 seconds
            if (int(tdelta.seconds)-25200)>300:   
                print("Deleting file {}".format(str(z)))
                s3.Object(buck,z).delete()
    except:
        print("Please check Internet connection.")