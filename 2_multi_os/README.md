## 2. Get structured show command output for multiple OS (XE and XR)

In the third exercice, we will connect on multiple devices of the same testbed. They are running different OS (XE and XR). We will see that we can get the same structured output with the same line of code.

### Output example

```
-----------------------------------
-- Connected on device: csr1000v --
-----------------------------------
Loopback333 -- 3.3.3.3
Loopback99 -- 99.99.99.99
Loopback11 -- 1.2.3.1
GigabitEthernet2 -- Unassigned
GigabitEthernet1 -- 10.10.20.48
GigabitEthernet3 -- Unassigned

-----------------------------------
-- Connected on device: iosxr1 --
-----------------------------------
Loopback200 -- 1.1.1.200
Loopback100 -- 1.1.1.100
GigabitEthernet0/0/0/1 -- Unassigned
GigabitEthernet0/0/0/0 -- Unassigned
MgmtEth0/RP0/CPU0/0 -- 10.10.20.175
Null0 -- Unassigned
```

## Folders

The file with the exercise is in the `exercise` folder. An example of solution can be found in the `solution_example` folder.

# Steps

**Please note that we are now using the `Genie` library!**

The testbed is already loaded for you. Fore more information about the `topology.loader.load()` API, please refer to the documentation below:

> https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#testbed-file


The below arguments avoid pritting the `show version`, `show running-configuration` and the output.

```python
device.connect(init_exec_commands=[],
               init_config_commands=[],
               log_stdout=False)
```

### Step 0: load the testbed

From the `genie` module, we import the `testbed.load()` function. This function will be used to load the testbed file we have created.

We load the `testbed` information, stored in our `testbed.yaml` file. We assign it to an object: `testbed`.

### Step 1: iterate through each device in the testbed

`testbed` object has an `iterator` capability. When used, it returns each `device` object in the testbed. We will iterate through each device in the testbed, connect and populate our model.

### Step 2: connect to the device

We use the `connect()` method on the `iosxr1` object to connect to the device.

By default, pyATS will send exec and configuration commands to the device (such as `terminal length 0` and `show version`). To avoid such behavior, we are passing arguments to the `conect()` method. We are also disabling the logging to standard output.
More information in the [documentation].(https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html)
{: .notice--info}

### Step 3: learn `interface` model from the device

This step is the most important step in our script. It will `Learn` the `interface` model. pyATS will send **multiple show-commands** to the device in order to fully populate the model. Each information of the CLI output will be mapped either as a dictionary key or a value. Because we need to have the same keys between models, there could be entropy loss between the raw CLI output and the parsed output. For example, if an operational data is unique to an OS.

To do so, we are using the `learn()` method on the `device` object. The `learn` method takes a string as parameter, which is the model we would like to collect and parse. We are saving this parsed output in a variable `show_interface`.

You can find all pyATS supported **models** in the [official documentation](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models).
{: .notice--info}

A parsed output example (i.e. the dictionary saved in the variable `show_interface`) can be seen in **Step 4**. 

### Step 4: Python logic to print interface name and IP

Below an example of parsed output for the `interface` model. Most interfaces are **missing** (only one is shown), for conciseness.

**Parsed CLI output**
{: .notice--primary}
<div class="highlighter-rouge">
<pre class="highlight">
<code>
{'GigabitEthernet0/0/0/0': {'bandwidth': 1000000,
                            'counters': {'in_broadcast_pkts': 0,
                                         'in_crc_errors': 0,
                                         'in_discards': 0,
                                         'in_multicast_pkts': 0,
                                         'in_octets': 0,
                                         'in_pkts': 0,
                                         'last_clear': 'never',
                                         'out_broadcast_pkts': 0,
                                         'out_errors': 0,
                                         'out_multicast_pkts': 0,
                                         'out_octets': 0,
                                         'out_pkts': 0,
                                         'rate': {'in_rate': 0,
                                                  'in_rate_pkts': 0,
                                                  'load_interval': 300,
                                                  'out_rate': 0,
                                                  'out_rate_pkts': 0}},
                            'enabled': False,
                            'encapsulation': {'encapsulation': 'arpa'},
                            'flow_control': {'flow_control_receive': False,
                                             'flow_control_send': False},
                            'ipv6': {'enabled': False},
                            'mac_address': '0050.56bb.4247',
                            'mtu': 1514,
                            'oper_status': 'down',
                            'phys_address': '0050.56bb.4247',
                            'type': 'gigabitethernet'}
</code>
</pre>
</div>

In the above output, we have a list of interfaces: `GigabitEthernet0/0/0/0` (others are **not** shown for conciseness). We are iterating through this list. For each interface, we are accessing the `ip_address` value. We're then printting the interface `name` and `IP`. 

The `info` attribute of the `Interface` object returns a Python dictionnary. We are iterating through this dictionnary items. It's return all the `tuples` of `key: values` of this dictionnary.

It might not be useful in a real life use case. Goal here is to take a concise example, to show how easy it is to extract values of a CLI output when parsed with pyATS libraries.
{: .notice--info}

### Step 5: disconnect from the device

We use the `disconnect()` method to properly disconnect from the device. 

It’s important to properly disconnect from the device, otherwise the vty connection will remain open on the device, until it times out.
{: .notice--info}