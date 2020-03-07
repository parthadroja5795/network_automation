#script to generate JSON file containing all SSH login information

#!/usr/bin/env python

import json
    
if __name__ == "__main__":
    
    ssh_info={}
     
    Edge1={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.10'
        }
     
    Edge2={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.20'
        }
     
    Edge3={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.50'
        }
     
    Edge4={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.60'
        }
    
    Core1={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.30'
        }
    
    Core2={'device_type':'cisco_ios',
        'username':'netman',
        'password':'netman',
        'ip':'198.51.100.40'
        }
    
    ssh_info['Edge1']=Edge1
    ssh_info['Edge2']=Edge2
    ssh_info['Edge3']=Edge3
    ssh_info['Edge4']=Edge4
    ssh_info['Core1']=Core1
    ssh_info['Core2']=Core2
    
    #saving the SSH login information in a file
    file_name=open("netman_lab10_sshInfo.json",'w')
    json.dump(ssh_info,file_name)
    file_name.close()