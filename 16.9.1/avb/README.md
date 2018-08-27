#### AVB 
Python scripts related to Audio Video Briding (IEEE 802.1BA) support on Catalyst Platforms.
For details, refer to: http://www.cisco.com/go/avb   

#### auto_avb.py
Script automating the deployemt of AVB networks. Push all AVB related configurations to multiple
switches with single script execution. The automation also handles feature dependencies.

#### Usage
```
python auto_avb.py <path/to/inventory/xl> <username> <password> mvrp_enable|mvrp_disable
```
<path/to/inventory/xl> : Path to local XL file with network inventory details
<username> : Username for switch login (common for all switches)
<password> : Password for siwtch login (common for all switches)
mvrp_enable|mvrp_disable : MVRP enable or disable based on requirement

#### Examples 
To deploy AVB where endpoints use MVRP:
```
python auto_avb.py /home/<dir>/<subdir>/inventory.xlsx admin password mvrp_enable
```
To deploy AVB where endpoints do not use MVRP:
```
python auto_avb.py /home/<dir>/<subdir>/inventory.xlsx admin password mvrp_disable
```

#### Notes
XL format:
```
IP		Interfaces
10.104.55.61	11,12,13
10.104.55.62	14,15,16
10.104.55.63	17,18,19
```

### Enhancements / Todo's
- Support for all types of interfaces (currently script uses "TenGigabitEthernet")
- Support for auto detection and configuration of downlink ports as well as interconnects


