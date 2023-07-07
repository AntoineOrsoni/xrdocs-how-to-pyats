## TODO rename XRD-1 XRD-source so we are using the exact same name everywhere

# import the aetest module
from pyats import aetest
import logging
import re
import xmltodict

logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):
    
    @aetest.subsection
    def connect_to_devices(self, nodes):
        
        for device in nodes.values():
            # don't do the default show version
            # don't do the default config
            device.connect(log_stdout=False,
                           learn_hostname=True,
                           via='netconf')
            
            device.connect(log_stdout=False,
                           learn_hostname=True,
                           via='cli')
            
            if device.cli.connected and device.netconf.connected:
                logger.info(f'{device.alias} connected. CLI: {``device.cli.connected``} - NETCONF: {device.netconf.connected}')
            else:
                logger.warning(f'{device.alias} not connected. CLI: {device.cli.connected} - NETCONF: {device.netconf.connected}')
                self.failed(f'Could not connect to {device.alias}')

        self.passed('All devices are connected')

    @aetest.subsection
    def check_startup_config(self, nodes):
        
        for device in nodes.values():

            # Checking if we have less or more than exactly one startup file
            pattern = 'xrd-.*-startup.cfg'
            rpc_request = '''
            <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
            <get>
                <filter>
                <dir xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-dir-oper">
                    <nodes>
                    <node>
                        <node-name>0/RP0/CPU0</node-name>
                        <dir-paths>
                        <dir-path>
                            <name>harddisk:</name>
                        </dir-path>
                        </dir-paths>
                    </node>
                    </nodes>
                </dir>
                </filter>
            </get>
            </rpc>
            '''

            reply = xmltodict.parse(device.netconf.request(rpc_request, timeout=120))
            files = [content['name'] for content in reply['rpc-reply']['data']['dir']['nodes']['node']['dir-paths']['dir-path']['directory']['content']]
            count_startup_config = len([key for key in files if re.match(pattern, key)])

            if count_startup_config != 1:
                self.failed(f'{device.alias} has no unique startup file. Count = {count_startup_config}')
            else:
                logger.info(f'{device.alias} has a unique startup-config file.')
                device.startup_config = [key for key in files if re.match(pattern, key)][0]

        self.passed('All devices have unique startup-config file.')

    @aetest.subsection
    def clean_config(self, nodes):

        for device in nodes.values():
            device.cli.configure(f'''
                load harddisk:{device.startup_config}
                commit replace
                ''')

    @aetest.subsection
    def initial_traceroute(self, nodes):

        rpc_request = '''
        <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
            <traceroute xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-traceroute-act">
                <destination>
                <destination>10.3.1.3</destination>
                </destination>
            </traceroute>
        </rpc>
        '''

        source = nodes['xrd-source']
        reply = xmltodict.parse(source.netconf.request(rpc_request, timeout=120))

        expected_hops = ['10.1.1.3',
                        '100.101.103.103',
                        '100.103.104.104',
                        '100.102.104.102',
                        '10.3.1.3']
        
        hops = []

        for hop in reply['rpc-reply']['traceroute-response']['ipv4']['hops']['hop']:
            hops.append(hop['hop-address'])

        if hops == expected_hops:
            self.passed(f'Path is right.\nExpected: {expected_hops}.\nGot: {hops}.')
        else:
            self.failed(f'Path is wrong.\nExpected: {expected_hops}.\nGot: {hops}.')


class Check_SR_Policy(aetest.Testcase):

    @aetest.test
    def push_sr_policy(self, nodes):

        xrd1 = nodes['xrd-1']
        xrd1.cli.configure('''
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
        
    @aetest.test
    def policy_traceroute(self, nodes):

        rpc_request = '''
        <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101">
            <traceroute xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-traceroute-act">
                <destination>
                <destination>10.3.1.3</destination>
                </destination>
            </traceroute>
        </rpc>
        '''

        source = nodes['xrd-source']
        reply = xmltodict.parse(source.netconf.request(rpc_request, timeout=120))

        expected_hops = ['10.1.1.3',
                        '100.101.103.103',
                        '100.103.105.105',
                        '100.105.106.106',
                        '100.104.106.104',
                        '100.102.104.102',
                        '10.3.1.3']
        
        hops = []

        for hop in reply['rpc-reply']['traceroute-response']['ipv4']['hops']['hop']:
            hops.append(hop['hop-address'])

        if hops == expected_hops:
            self.passed(f'Path is right.\nExpected: {expected_hops}.\nGot: {hops}.')
        else:
            self.failed(f'Path is wrong.\nExpected: {expected_hops}.\nGot: {hops}.')

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def clean_config(self, nodes):

        for device in nodes.values():
            device.cli.configure(f'''
                load harddisk:{device.startup_config}
                commit replace
                ''')

    @aetest.subsection
    def disconnect_from_devices(self, nodes):
        
        for device in nodes.values():
            device.disconnect()

if __name__ == '__main__':

    # local imports
    from genie import testbed

    # set debug level DEBUG, INFO, WARNING
    logger.setLevel(logging.INFO)

    testbed = testbed.load('/Users/anorsoni/Documents/Programmability/XRDocs/how-to-pyATS/4_aetest/testbed.yaml')
    
    xrd1 = testbed.devices['xrd1']
    source = testbed.devices['xrd-source']
    
    nodes = {'xrd-1': xrd1, 'xrd-source': source}

    aetest.main(nodes = nodes)