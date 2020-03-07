#script to generate real-time network monitoring dashboard using SNMP and send an automated alert for any faults

#!/usr/bin/env python

import subprocess
import smtplib

#function to send the email notification
def mail(x,y):

    msg="This is an automated from the NMS."+y+" is down on "+x+". Please check."

    fromaddr="sender email address"
    toaddrs="receiver email address"

    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    username="sender email address"
    password="sender email password"
    server.login(username,password)

    server.sendmail(fromaddr,toaddrs,msg)
    server.quit()

if __name__ == "__main__":

    #monitoring the network in real-time
    while(1):
        o1=['R1']
        o2=['R2']
        o3=['R3']
        
        #list of OIDs being monitored
        oid=['ifName.1','ifAlias.1','ifOperStatus.1','ifPhysAddress.1','ifAdminStatus.1','ifInUcastPkts.1','ipAdEntAddr','ipAdEntNetMask']
        
        #sending SNMP request to fetch required information
        for i in oid:
            if i=='ipAdEntAddr' or i=='ipAdEntNetMask':
                x1=subprocess.Popen(['snmpbulkwalk','-v','2c','-c','public','198.51.100.3',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            else:
                x1=subprocess.Popen(['snmpget','-v','1','-c','public','198.51.100.3',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            y1=x1.stdout.read().strip()
            if y1[0:7]=="Timeout":
                o1.append("Check Mgt. Int")
            else:
                z1=y1.split("=")
                w1=z1[1].split(":")
                if len(w1)==2:
                    o1.append(w1[1])
                else:
                    s=":"
                    r1=s.join(w1[1:])
                    o1.append(r1)
    
        for i in oid:
            if i=='ipAdEntAddr' or i=='ipAdEntNetMask':
                x2=subprocess.Popen(['snmpbulkwalk','-v','2c','-c','public','198.51.100.4',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            else:
                x2=subprocess.Popen(['snmpget','-v','2c','-c','public','198.51.100.4',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            y2=x2.stdout.read().strip()
            if y2[0:7]=="Timeout":
                o2.append("Check Mgt. Int")
            else:
                z2=y2.split("=")
                w2=z2[1].split(":")
                if len(w2)==2:
                    o2.append(w2[1])
                else:
                    s=":"
                    r2=s.join(w2[1:])
                    o2.append(r2)
    
        for i in oid:
            if i=='ipAdEntAddr' or i=='ipAdEntNetMask':
                x3=subprocess.Popen(['snmpbulkwalk','-v','3','-l','priv','-u','Parth_User','-a','md5','-A','Parth_AUTHPW','-x','des','-X','Parth_PRIVPW','198.51.100.5',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            else:
                x3=subprocess.Popen(['snmpget','-v','3','-l','priv','-u','Parth_User','-a','md5','-A','Parth_AUTHPW','-x','des','-X','Parth_PRIVPW','198.51.100.5',i],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            y3=x3.stdout.read().strip()
            if y3[0:7]=="Timeout":
                o3.append("Check Mgt. Int")
            else:
                z3=y3.split("=")
                w3=z3[1].split(":")
                if len(w3)==2:
                    o3.append(w3[1])
                else:
                    s=":"
                    r3=s.join(w3[1:])
                    o3.append(r3)
    
        #printing the dashboard
        print("Router".rjust(20)+"Interface ID".rjust(20)+"Desription".rjust(20)+"Op._Status".rjust(20)+"Physical Address".rjust(20)+"Admin Status".rjust(20)+"Packet Counter".rjust(20)+"Interface IP".rjust(20)+"Subnet Mask".rjust(20))
        print(o1[0].rjust(20)+o1[1].rjust(20)+o1[2].rjust(20)+o1[3].rjust(20)+o1[4].rjust(20)+o1[5].rjust(20)+o1[6].rjust(20)+o1[7].rjust(20)+o1[8].rjust(20))
        print(o2[0].rjust(20)+o2[1].rjust(20)+o2[2].rjust(20)+o2[3].rjust(20)+o2[4].rjust(20)+o2[5].rjust(20)+o2[6].rjust(20)+o2[7].rjust(20)+o2[8].rjust(20))
        print(o3[0].rjust(20)+o3[1].rjust(20)+o3[2].rjust(20)+o3[3].rjust(20)+o3[4].rjust(20)+o3[5].rjust(20)+o3[6].rjust(20)+o3[7].rjust(20)+o3[8].rjust(20))
        
        #if fault is detected then send an automated alert
        if o1[3]!=' up(1)':
            print("{} is down on {}. Please check.".format(o1[2],o1[0]))
            mail(o1[0],o1[2])
        elif o2[3]!=' up(1)':
            print("{} is down on {}. Please check.".format(o2[2],o2[0]))
            mail(o2[0],o2[2])
        elif o3[3]!=' up(1)':
            print("{} is down on {}. Please check.".format(o3[2],o3[0]))
            mail(o3[0],o3[2])