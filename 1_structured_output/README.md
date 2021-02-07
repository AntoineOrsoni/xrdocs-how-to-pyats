This example is further detailed in the blog post below.

> https://xrdocs.io/programmability/tutorials/pyats-series-parsing-like-a-pro

# 1. Get structured show command output

In the second exercice, we will leverage Genie parsers to get a structured output (JSON). Complete list of interfaces.

## Output example

The below output might differ, depending on the device's current configuration.

```
Loopback333 -- 3.3.3.3
Loopback99 -- 99.99.99.99
Loopback11 -- 1.2.3.1
GigabitEthernet2 -- Unassigned
GigabitEthernet1 -- 10.10.20.48
GigabitEthernet3 -- Unassigned
```

## Steps

**Please note that we are now using the `Genie` library!**

The testbed is already loaded for you. Fore more information about the `topology.loader.load()` API, please refer to the documentation below:

> https://pubhub.devnetcloud.com/media/pyats/docs/topology/creation.html#testbed-file

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

Use the `parse()` method on the `iosxr1` object to send a CLI command to the device. Get the `show interface brief` output, and save it in a variable. This output will be parsed using Genie libraries. We are saving the output in a dictionnary variable: `show_interface`. Each valuable information in the output will be mapped as a pair of `key: value`.

You can read more about the `parse()` method in the documentation:

> https://pubhub.devnetcloud.com/media/genie-docs/docs/cookbooks/explore.html?highlight=parse#

Available parsers can be found here:

> https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers

### Step 4

Use a loop to iterate through your list of `interfaces`. Print each interface name and its IP address. Refer to the output example, above.

### Step 5

Use the `disconnect()` method to disconnect from `iosxr1`.