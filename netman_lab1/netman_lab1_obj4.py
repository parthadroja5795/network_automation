#script to parse wireshark to get SNMP trap information and send email notification using SMTP

#!/usr/bin/env python

from scapy.all import *
import smtplib

if __name__ == "__main__":
    
    i=0
    a = rdpcap("netman_lab1_obj4.pcap")
    snmp_trap=[]
    
    #parsing the wireshark capture to get the SNMP trap information
    for line in a:
        try:
            if a[i][UDP].dport==162:
                l2=line
                l3=l2.payload
                l4=l3.payload
                l5=l4.payload
                l6=str(l5.show)
                snmp_trap.append(l6)
                i=i+1
        except:
            continue
    
    msg=str(snmp_trap)
    
    #sending the email using the SMPT
    fromaddr="sender email address"
    toaddrs="receiver email address"
    
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    username="sender email address"
    password="sender email password"
    server.login(username,password)
    
    server.sendmail(fromaddr,toaddrs,msg)
    server.quit()