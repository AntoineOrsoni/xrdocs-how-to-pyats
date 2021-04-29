# New module! Now using Genie!
from genie import testbed

# Step 0: Load the testbed
testbed = testbed.load('./testbed.yaml')

# Step 1: Iterate through each device in the testbed
for device in testbed:

    print('')

    # Step 2: Connect on the device and print its name
    device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)
    
    print('-----------------------------------')
    print('-- Connected on device: {device} --'.format(device=device.alias))
    print('-----------------------------------')

    # Step 3: Learn interface model from the device
    show_interface = device.learn('interface')

    for interface, info in show_interface.info.items():

        # Step 4: What if the key 'ipv4' doesn't exist (= no assigned IPv4)?
        if 'ipv4' in info:
            for ip, value in info['ipv4'].items():
                print('{interface} -- {ip}'.format(interface=interface, ip=value['ip']))
        else:
            print('{interface} -- Unassigned'.format(interface=interface))
    
    print('')

    # Step 5: Disconnect from the device
    device.disconnect()