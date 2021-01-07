# Intro

This repo is mainly inspired of [this repo](https://github.com/AntoineOrsoni/pyats-devnet-se-hour) on IOS XE. 

It gives an overview of pyATS possibilities. As any overview, it's not intended to be exhaustive.

# Pre-requisites
## Testbed

We're using the always-on DevNet sandboxes in the `testbed.yaml` file. More information about DevNet sandboxes here:

> http://devnetsandbox.cisco.com/RM/Topology

We will be using the IOS XR sandbox for the exercices attached. Feel free to use others.

## Dependances

To install the right packages, please run the command below:

```
pip install -r requirements.txt
```

# Exercices
## 0. Get CLI show command output

In the first exercice, we will connect to the device and get an unstructued show command output (ex: `show ip interface brief`).

### Output example

```
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       10.10.20.48     YES other  up                    up      
GigabitEthernet2       unassigned      YES NVRAM  administratively down down    
GigabitEthernet3       unassigned      YES NVRAM  up                    up      
Loopback11             1.2.3.1         YES other  up                    up  
```

### Complete instructions

[Complete instructions can be found here](0_get_cli_show/README.md)

# pyATS documentation
## Official documentation

pyATS documentation can be found here:

> https://pubhub.devnetcloud.com/media/pyats/docs/getting_started/index.html

## List of supported platforms

The list of supported platforms can be found here:

> https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/supported_platforms.html

## Typical errors

Below a list of errors I encountered and the resolution. The list is not aimed to be exhaustive.

### Testbed file is not in the folder of execution

```
! output omitted
pyats.utils.yaml.exceptions.LoadError: Content of 'testbed.yaml' failed to load into a dict.
```

### Hostname and testbed mismatch

The name of the device in your testbed, and the hostname MUST match. It's case sensitive.

```
unicon.core.errors.TimeoutError: timeout occurred:
```

Otherwise, you can also set the `learn_hostname` argument to `True`.

```python
device.connect(learn_hostname=True)
```

More information in the documentation below:

> https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html

### Don't print the default commands

Don't print the `show version`, `show running-configuration` and the output.

```python
device.connect(init_exec_commands=[],
               init_config_commands=[],
               log_stdout=False)
```

### device.learn('platform')

`platform.os` has the following values for IOSXE and IOSXR:
- `iosxe` >> lower case
- `IOSXR` >> upper case

### diconnect() quickly

To avoid waiting ~10 seconds to disconnect on the device, you can edit your `testbed.yaml` file as such:

```yaml
    connections:
      cli:
        protocol: telnet
        ip: 10.1.1.1
        settings:
          GRACEFUL_DISCONNECT_WAIT_SEC: 0
          POST_DISCONNECT_WAIT_SEC: 0
```

More info here:

> https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/connection.html