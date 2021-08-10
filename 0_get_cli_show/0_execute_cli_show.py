from pyats.topology import loader

# Step 0: load the testbed
testbed = loader.load('./testbed.yaml')

# Step 1: testbed is a dictionary. Extract the device iosxr1
iosxr1 = testbed.devices["iosxr1"]

# Step 2: Connect to the device
iosxr1.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False, learn_hostname=True)

# Step 3: saving the `show ip interface brief` output in a variable
show_interface = iosxr1.execute('show ip interface brief')

# Step 4: pritting the `show interface brief` output
print(show_interface)

# Step 5: disconnect from the device
iosxr1.disconnect()
