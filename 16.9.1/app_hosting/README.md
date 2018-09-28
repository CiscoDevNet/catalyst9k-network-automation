# Application Hosting 
Python scripts related to Application Hosting support on Catalyst 9K Platforms.

# apphostingresource.py
Script automating the CPU and Memory allocation changes for particular application.

# Usage
```
python apphostingresource.py --host <ip address> -u <username> -p <password> -a <application_name> -m <memory_allocation> -c <cpu_allocation>
```

<username> : Username for switch login (common for all switches)
<password> : Password for switch login (common for all switches)
<application_name> : Name of the application 
<memory allocation> : Memory resource in MB (0-4096)
<cpu allocation> : CPU resource in CPU units (0-7400)


# Examples 
To change CPU and Memory of the application.
```
python apphostingresource.py --host 128.26.20.246 -u cisco -p cisco -a iperf -m 20 -c 600

```

#### Notes
This automation will work only if application is already installed on Catalyst 9K switch and it should be “Deployed” state. After that, Application needs to “Running” State to see new CPU and memory allocation.

# app-hosting_networking.py
Script automating the IP address, Mask and Gateway of the application.

# Usage
```
python app-hosting_networking.py --host <ip address> -u <username> -p <password> -a <application_name> -i <ip_address> -m <mask> -g <gateway>
```

<username> : Username for switch login (common for all switches)
<password> : Password for switch login (common for all switches)
<application_name> : Name of the application 
<IP> : IP address of the application
<Mask> : Mask of the application
<Gateway> :default gateway of the application.


# Examples 
To change IP address, mask and default gateway of the application.
```
python app-hosting_networking.py --host 128.26.20.246 -u cisco -p cisco -a iperf -i 12.0.0.2 -m 255.255.255.0 -g 12.0.0.1

```

#### Notes
This automation will work only if application is already installed on Catalyst 9K switch and it should be “Deployed” state. After that, Application needs to “Running” State to see new CPU and memory allocation.
