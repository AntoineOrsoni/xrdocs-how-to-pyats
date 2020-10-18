# New module! Now using genie!
from genie.testbed import load

# Loading device information
testbed = load('testbed.yaml')
csr1000v = testbed.devices["csr1000v"]

# Connect to the device
csr1000v.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)

# Step 0: showing the output in the terminal output
show_interface = csr1000v.parse('show ip interface brief')
print(show_interface)

# Step 1: For each interface, give the interface name + IP address
for interface in show_interface['interface']:
    print('{interface} -- {ip}'.format(interface=interface, 
                                       ip=show_interface['interface'][interface]['ip_address']))
