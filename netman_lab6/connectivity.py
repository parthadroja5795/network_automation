#script to check whether the IP address is reachable or not

#!/usr/bin/env python

import json
import os
import socket
import subprocess

#function to check the reachability of the IP address
def check_connectivity(ip):

	test_ip=ip
	proc = subprocess.Popen( ['ping', '-c', '2', test_ip], stdout=subprocess.PIPE)
	sdout, stderr = proc.communicate()
	if proc.returncode == 0:
		print("{} is reachable.".format(test_ip))
	else:
		print("{} is not reachable.".format(test_ip))