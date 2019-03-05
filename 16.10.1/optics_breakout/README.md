# Configuring breakout in C9500-32C
Python scripts related to configuring breakout in C9500-32C.
# optics.py
Script automating to configure breakout cable on C9500-32C by checking supported optics list and checking breakout capable ports.
Note: Not every ports on C9500-32C is breakout capable with 16.10 release.
# Usage
python optics.py --host <ip address> -u <username> -p <password> -i <interface_name> 
: Username for switch login (common for all switches) : Password for switch login (common for all switches) <interface_name> : name of the interace
# Examples
To configure breakout on HundredGigE 1/0/1.
python optics.py --host 172.26.196.48 -u cisco -p cisco -i HundredGigE1/0/1 


