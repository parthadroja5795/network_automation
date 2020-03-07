#script to push and poll configuration using NETCONF

#!/usr/bin/env python

from ncclient import manager
from prettytable import PrettyTable
    
if __name__ == "__main__":
	
	#specifying the SSH IPs
	ssh_ip=["198.51.100.10","198.51.100.20","198.51.100.30","198.51.100.40","198.51.100.50"]
	
	#specifying required config information
	hostname=["Router1-paad0052","Router2-paad0052","Router3-paad0052","Router4-paad0052","Router5-paad0052"]
	ip=["10.1.1.1","10.1.2.1","10.1.3.1","10.1.4.1","10.1.5.1"]
	mask="255.255.255.0"
	interface="Loopback99"
	wildcard="0.0.0.255"
	networks=["10.1.1.0","10.1.2.0","10.1.3.0","10.1.4.0","10.1.5.0"]
	area="0"
	routers=["R1","R2","R3","R4","R5"]
	
	#configuration template in YANG format
	configuration="""
	<config>
	<cli-config-data>
	<cmd> hostname %s </cmd>
	<cmd> interface %s </cmd>
	<cmd> ip address %s %s </cmd>
	<cmd> router ospf 1 </cmd>
	<cmd> network %s %s area %s </cmd>
	<cmd> network 198.51.100.0 0.0.0.255 area 0 </cmd>
	</cli-config-data>
	</config>
	"""
	
	#pushing config to the routers	
	for i in range(0,5):
		
		#generating the configuration from the template
		config_str = configuration % (hostname[i],interface,ip[i],mask,networks[i],wildcard,area)
		
		#opening the NETCONF connection
		conn=manager.connect(host=ssh_ip[i],port=22,username="netman",password="netman",hostkey_verify=False,device_params={'name':'iosxr'},allow_agent=False,look_for_keys=True)
		print("Connected to {} and configuring.".format(routers[i]))
		
		#pushing the configuration
		rpc_sent=conn.edit_config(target="running",config=config_str)
		print("Configuration done on {}".format(routers[i]))
	
	#polling the configuration and printing in a table format
	table=PrettyTable(["Router","Hostname","Loopback 99 IP","OSPF networks"])
	
	for i in range(0,5):
		print("Fetching data from {}".format(routers[i]))
		
		#opening the NETCONF connection
		conn=manager.connect(host=ssh_ip[i],port=22,username="netman",password="netman",hostkey_verify=False,device_params={'name':'iosxr'},allow_agent=False,look_for_keys=True)
		
		#getting the hostname
		hostname_filter = '''
		<filter>
		<config-format-text-cmd>
		<text-filter-spec> | inc hostname </text-filter-spec>
		</config-format-text-cmd>
		</filter>
		'''
		result1 = conn.get_config("running",hostname_filter)
		z=str(result1).split()
		o1=z[5]
	
		#getting the loopback99 information
		interface_filter='''
		<filter>
		<config-format-text-block>
		<text-filter-spec> interface Loopback99 </text-filter-spec>
		</config-format-text-block>
		</filter>
		'''
		result2= conn.get_config("running",interface_filter)
		y=str(result2).split()
		o2=y[9]+"/24"
	
		#getting the OSPF information
		ospf_filter='''
		<filter>
		<config-format-text-cmd>
		<text-filter-spec> | inc network </text-filter-spec>
		</config-format-text-cmd>
		</filter>
		'''
		result3= conn.get_config("running",ospf_filter)
		x=str(result3).split()
		o3=x[6]+"/24 area "+x[9],x[13]+"/24 area "+x[16]
		
		table.add_row((routers[i],o1,o2,o3))
	
	#printing the polled information in a table format
	print(table)