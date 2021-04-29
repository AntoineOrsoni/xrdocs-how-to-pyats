# New module! Now using Genie!
from genie import testbed

# Step 0: load the testbed
testbed = testbed.load('./testbed.yaml')

# Step 1: testbed is a dictionary. Extract the device iosxr1
iosxr1 = testbed.devices["iosxr1"]

# Step 2: Connect to the device
iosxr1.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)

# Step 3: saving the `show ip interface brief` output in a variable
show_interface = iosxr1.parse('show ip interface brief')

# Step 4: iterating through the parsed output. Extracting interface name and IP
for interface in show_interface['interface']:
    print(f"{interface} -- {show_interface['interface'][interface]['ip_address']}")

# Step 5: disconnect from the device
iosxr1.disconnect()