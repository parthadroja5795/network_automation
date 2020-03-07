#script to find the MAC addresses from IPv6 tcpdump

#!/usr/bin/env python

from scapy.all import *

#function to convert from EUI-64 to MAC address
def eui64_to_mac(temp):
    final=[]
    mac=[]

    #removing the FF and FE which are added during MAC to EUI-64 conversion
    x1=temp[5].replace("ff", "");
    x2=temp[6].replace("fe", "");
    
    #inverting the 7th bit
    x3=list(temp[4])
    if x3[1]=='0':
        x3[1]='2'
    elif x3[1]=='1':
        x3[1]='3'
    elif x3[1]=='2':
        x3[1]='0'
    elif x3[1]=='3':
        x3[1]='1'
    elif x3[1]=='4':
        x3[1]='6'
    elif x3[1]=='5':
        x3[1]='7'
    elif x3[1]=='6':
        x3[1]='4'
    elif x3[1]=='7':
        x3[1]='5'
    elif x3[1]=='8':
        x3[1]='a'
    elif x3[1]=='9':
        x3[1]='b'
    elif x3[1]=='a':
        x3[1]='8'
    elif x3[1]=='b':
        x3[1]='9'
    elif x3[1]=='c':
        x3[1]='e'
    elif x3[1]=='d':
        x3[1]='f'
    elif x3[1]=='e':
        x3[1]='c'
    elif x3[1]=='f':
        x3[1]='f'
    
    #combining all the components of MAC address
    final.append(''.join(x3))
    final.append("".join(x1+x2))
    final.append(temp[7])
    
    #padding 0's wherever its needed
    for i in final:
        mac.append(i.zfill(4))
    
    final_mac=".".join(mac)
    return final_mac

#function t extract MAC address
def get_mac_address(file):
    
    #reading the tcpdump file
    a = adpcap(file)
    i=0
    temp=[]
    MAC=[]
    for line in a:
        try:
            #finding ICMPv6 echo request
            if(a[i][ICMPv6EchoRequest].type==128):
                temp.append(a[i][IPv6].src)
        except:
            pass
        i=i+1
    
    z=set(temp)
    MAC=list(z)
    
    x=MAC[1].split(":")
    y=MAC[0].split(":")
    
    #converting from EUI-64 to MAC address
    r2_mac=eui64_to_mac(x)
    r3_mac=eui64_to_mac(y)
    
    print("MAC address of R2 is: {}".format(r2_mac))
    print("MAC address of R3 is: {}".format(r3_mac))