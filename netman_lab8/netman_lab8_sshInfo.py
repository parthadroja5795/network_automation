#script to generate JSON file containing all SSH login information

#!/usr/bin/env python

import json

if __name__ == "__main__":
    
    ssh_info={}
    
    R1={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.10'
        }
    
    R2={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.20'
        }
    
    R3={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.30'
        }
    
    ssh_info['R1']=R1
    ssh_info['R2']=R2
    ssh_info['R3']=R3
    
    #saving the SSH login information in a file
    file_name=open("netman_lab8_sshInfo.json",'w')
    json.dump(ssh_info,file_name)
    file_name.close()