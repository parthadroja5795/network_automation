#script to check whether the IP address is valid or not

#!/usr/bin/env python

import json
import os
import socket
import sys

#function to check the validity of the IP address
def validateIP(ip):
	test_ip=ip
	try:
		socket.inet_aton(test_ip)
		print("{} is a valid IP address.".format(test_ip))
	except:
		print("{} is an invalid IP address.".format(test_ip))