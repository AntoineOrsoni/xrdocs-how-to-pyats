This example is further detailed in the blog post below.

> https://xrdocs.io/programmability/tutorials/pyats-series-install-and-use-pyats/

# 0. Get CLI show command output

In the first exercice, we will connect to the device and get an unstructued show command output (ex: `show ip interface brief`).

## Output example

```
Interface                      IP-Address      Status          Protocol Vrf-Name
Loopback100                    1.1.1.100       Up              Up       default 
Loopback200                    1.1.1.200       Up              Up       default 
Loopback999                    unassigned      Up              Up       default 
MgmtEth0/RP0/CPU0/0            10.10.20.175    Up              Up       default 
GigabitEthernet0/0/0/0         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/1         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/2         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/3         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/4         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/5         unassigned      Shutdown        Down     default 
GigabitEthernet0/0/0/6         unassigned      Shutdown        Down     default
```

## Steps

### Step 0

Load the testbed. Use the `loader.load()` API. Fore more information about the `topology.loader.load()` API, please refer to the documentation below:

> https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#testbed-file

### Step 1

A `testbed` is a `pyats.topology.testbed.Testbed` object. It has a `devices` attribute, which is a dictionnary of all devices in the testbed. 
* Try to print it.
* Extract the `iosxr1` device. 

### Step 2

Connect to the device. Use the `connect()` method to do so. It's explained here:

> https://pubhub.devnetcloud.com/media/pyats/docs/connections/manager.html#method-instantiate-connect

The below arguments avoid pritting the `show version`, `show running-configuration` and the output.

```python
device.connect(init_exec_commands=[],
               init_config_commands=[],
               log_stdout=False)
```

### Step 3

Use the `execute()` method on the `iosxr1` object to send a CLI command to the device. Get the `show interface brief` output, and save it in a variable.

More information about the `execute()` method here:

> https://pubhub.devnetcloud.com/media/pyats/docs/apidoc/connections/index.html#module-pyats.connections.bases

### Step 4

Print the output.

### Step 5

Use the `disconnect()` method to disconnect from `iosxr1`.