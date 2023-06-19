from genie import testbed

# Loading Testbed and Connecting to the device
testbed = testbed.load('/Users/anorsoni/Documents/Programmability/XRDocs/how-to-pyATS/5_config_builder/testbed.yaml')

xrd1 = testbed.devices["xrd1"]
source = testbed.devices["xrd-source"]
xrd1.connect(learn_hostname=True, log_stdout=False)
source.connect(learn_hostname=True, log_stdout=False)

print('xrd1 is connected =', xrd1.connected)
print('source is connected =', source.connected)


# Before
print('-- before changing SR policy.\n', source.execute('traceroute 10.3.1.3'))

print('\n\n\n')

# After
xrd1.configure('''
segment-routing
 traffic-eng
 segment-list 3-5-6-4-2
   index 10 mpls adjacency 100.100.100.103
   index 20 mpls adjacency 100.100.100.105
   index 30 mpls adjacency 100.100.100.106
   index 40 mpls adjacency 100.100.100.104
   index 50 mpls adjacency 100.100.100.102
  policy to-xrd-2
   color 10 end-point ipv4 100.100.100.102
   autoroute
    include ipv4 100.100.100.102/32
   !
   candidate-paths
    preference 100
     explicit segment-list 3-5-6-4-2
''')

print('-- after changing SR policy.\n', source.execute('traceroute 10.3.1.3'))
print('\n\n\n')


# Removing changes
xrd1.configure('load harddisk:xrd-1-startup.cfg\ncommit replace\n')
print('-- after cleaning.\n', source.execute('traceroute 10.3.1.3'))


xrd1.disconnect()
source.disconnect()