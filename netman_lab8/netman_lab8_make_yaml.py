#script to generate ansible var file from the given csv file

#!/usr/bin/env python

import os
import csv

if __name__ == "__main__":
    
    list2=[]
    
    #specifying the filename
    filename2="/etc/ansible/roles/router/vars/netman_lab8_main.yaml"
    b=open(filename2,'a')
    
    #opening the csv file
    filename="netman_lab8_config.csv"
    
    #reading the csv file and making set of all routers
    if os.path.isfile(filename):
        a=open(filename)
        csv_reader=csv.reader(a)
        for line in csv_reader:
            if line[0]!="Hostname":
                list2.append(line[0])
           
    routers=set(list2)
    a.close()
    
    #writing into the ansible var file
    line1="---\n"
    b.write(line1)
    line2="routers:\n"
    b.write(line2)
    
    filename="lab8.csv"
    if os.path.isfile(filename):
        for element in routers:
            line3=" - hostname: "+element+"\n"
            b.write(line3)
            a=open(filename)
            csv_reader=csv.reader(a)
        
            for line in csv_reader:
                if line[0]==element:
                    if line[1]=="Loopback":
                        
                        temp_process=line[5]
                        line4="   loopbackName: loopback {}\n".format(line[2])
                        b.write(line4)
                        
                        temp=line[3]
                        temp2=temp.split("/")
                        if temp2[1]=='32':
                            temp3="255.255.255.255"
                        line5="   loopbackIP: {} {}\n".format(temp2[0],temp3)
                        b.write(line5)
            a.close()
            
            line6="   processID: {}\n".format(temp_process)
            b.write(line6)
            
            line7="   interfaces:\n"
            b.write(line7)
            
            c=open(filename)
            csv_reader2=csv.reader(c)
            for line in csv_reader2:
                    if line[0]==element:
                        if line[1]=="FastEthernet":                
                            temp4=line[3]
                            temp5=temp4.split("/")
                            if temp5[1]=='24':
                                temp6="255.255.255.0"
                            line8="        - { name: "+line[2]+", IP: "+temp5[0]+" "+temp6+"} \n"
                            b.write(line8)
            c.close()
            
            line9="   ospfnetworks:\n"
            b.write(line9)
            
            d=open(filename)
            csv_reader3=csv.reader(d)
            for line in csv_reader3:
                    if line[0]==element:
                        temp7=line[3]
                        temp8=temp7.split("/")
                        if temp8[1]=='24':
                            temp9="0.0.0.255"
                        elif temp8[1]=="32":
                            temp9="0.0.0.0"
                        
                        line10="        - { IP: "+temp8[0]+" "+temp9+", area: "+line[6]+" }\n"
                        b.write(line10)
    
    #closing the files
    a.close()
    b.close()