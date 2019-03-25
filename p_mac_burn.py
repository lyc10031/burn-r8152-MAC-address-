#!/usr/local/bin/python3
import sys
import subprocess
from configparser import ConfigParser
from itertools import chain
import time



def call_func(eth_num,mac_list):
    for i,j in zip(range(eth_num),mac_list):
#	command = 'ls && date'
# 	result = subprocess.call(command,shell=True,stdout=subprocess.PIPE)
	command = f"rmmod r8152 && insmod burn_tools/r8152.ko && burn_tools/rtunicpg-x86_64 /# {i} /efuse /nodeid  {j}"
	result = subprocess.call(command,shell=True,stdout=subprocess.PIPE)
	print(result)





def calc_mac(mac,t):
	""" 
		Description: Calculate the MAC address to be burned 

		args: mac ,t
			mac :  current mac address
			t   :  The number of Mac addresses to calculate
 
		return: mac_list
	"""
	*base_num,last_two = mac.split(':')
	mac_list = [mac]
	for i in range(int(t)):
		if i == 0:
			new_last = hex(int(last_two,16)+1)
			if len(str(new_last)) == 1:
				new_last = '0' + new_last
			new = ':'.join(base_num)+':'+new_last.split('x')[1]
			# print(new)
			mac_list.append(new)
		else:
			new_last = hex(int(new[-2:],16)+1)
			if len(str(new_last)) == 1:
				new_last = '0' + new_last
			new = ':'.join(base_num)+':'+new_last.split('x')[1]	
			# print(new)		
			mac_list.append(new)
#	print(mac_list)
	return mac_list


def current_mac(status,future_mac=None):
    """
    Description: Read or Write files that record MAC addresses

    args: status,future_mac
       status: "r":read mac address from current_mac.conf
               "w":write write mac address to current_mac.conf
       future_mac: r -> None ,w -> Future MAC address

    return:  
        r:current_mac,
        w:write future_mac to current_mac.conf
    """

    file = 'current_mac.conf'   # mac地址配置文件
    cfg = ConfigParser()
    if status == 'r':
        with open(file,'r') as fp:
            cfg.read_file(chain(['[global]'], fp), source=file)
            current_mac = cfg.get('current_mac', 'mac1')
        return current_mac    

    elif status == 'w':
        cfg['current_mac'] = {"mac1":future_mac}
        with open(file,'w') as f:
            cfg.write(f)


def main(t):
    mac = current_mac("r") # read current mac address from current_mac.conf
    mac_list = calc_mac(mac,t)
    call_func(t,mac_list[:-1],)
    current_mac('w',mac_list[-1]) # write future mac address to current_mac.conf
	
if __name__ == '__main__':
#	mac = 'A0:98:05:02:B0:0F'
    args = sys.argv
    if len(args) != 2:
        print('Usage: \033[1;34;40mpython3 p_mac_burn.py (Number of network interfaces) \033[0m')
    else:
#        print(args)
        main(int(args[1]))
