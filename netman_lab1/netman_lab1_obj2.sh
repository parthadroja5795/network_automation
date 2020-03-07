#bash script to generate real-time network monitoring dashboard using SNMPv1, v2 and v3

#!/bin/bash

x=0

#reading OIDs to be monitored from a file
for i in `cat Parth_Netman1_Obj2`

#sending the SNMP requests to get the required information
do
    if [ $x -eq 0 ]
    then
	x1=$(snmpget -v 1 -c public 198.51.100.3 $i | awk '{print $4}')
        x6=$(snmpget -v 2c -c public 198.51.100.4 $i | awk '{print $4}')
        x11=$(snmpget -v 3 -l priv -u Parth_User -a md5 -A "Parth_AUTHPW" -x des -X "Parth_PRIVPW" 198.51.100.5 $i | awk '{print $4}')
        x=`expr $x + 1`
   elif [ $x -eq 1 ]
   then
        x2=$(cut -d "." -f 1 <<< `snmpget -v 1 -c public 198.51.100.3 $i| awk '{print $4}'`)
        x7=$(cut -d "." -f 1 <<< `snmpget -v 2c -c public 198.51.100.4 $i | awk '{print $4}'`)
        x12=$(cut -d "." -f 1 <<< `snmpget -v 3 -l priv -u Parth_User -a md5 -A "Parth_AUTHPW" -x des -X "Parth_PRIVPW" 198.51.100.5 $i | awk '{print $4}'`)
        x=`expr $x + 1`
   elif [ $x -eq 2 ]
   then
        x3=$(snmpget -v 1 -c public 198.51.100.3 $i | awk '{print $4}')
        x8=$(snmpget -v 2c -c public 198.51.100.4 $i | awk '{print $4}')
        x13=$(snmpget -v 3 -l priv -u Parth_User -a md5 -A "Parth_AUTHPW" -x des -X "Parth_PRIVPW" 198.51.100.5 $i | awk '{print $4}')
        x=`expr $x + 1`
   elif [ $x -eq 3 ]
   then    
        x4=$(snmpget -v 1 -c public 198.51.100.3 $i | awk '{print $4}')
        x9=$(snmpget -v 2c -c public 198.51.100.4 $i | awk '{print $4}')
        x14=$(snmpget -v 3 -l priv -u Parth_User -a md5 -A "Parth_AUTHPW" -x des -X "Parth_PRIVPW" 198.51.100.5 $i | awk '{print $4}')
        x=`expr $x + 1`
   else
        x5=$(snmpget -v 1 -c public 198.51.100.3 $i | awk '{print $5}')
        x10=$(snmpget -v 2c -c public 198.51.100.4 $i | awk '{print $5}')
        x15=$(snmpget -v 3 -l priv -u Parth_User -a md5 -A "Parth_AUTHPW" -x des -X "Parth_PRIVPW" 198.51.100.5 $i | awk '{print $5}')
   fi
done

#printing the gathered information
echo SNMPv1
echo Contact: $x1
echo Name: $x2
echo Location: $x3
echo Number: $x4
echo Uptime: $x5
echo 
echo SNMPv2
echo Contact: $x6
echo Name: $x7
echo Location: $x8
echo Number: $x9
echo Uptime: $x10
echo 
echo SNMPv3
echo Contact: $x11
echo Name: $x12
echo Location: $x13
echo Number: $x14
echo Uptime: $x15