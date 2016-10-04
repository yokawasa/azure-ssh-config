# azure-ssh-config

Generate SSH config file from Azure ARM VM inventry in subscription

## Introduction

azure-ssh-config is a simple script that collects Azure ARM Virtual Machine(VM) inventry in subscription and generate a SSH config entries to be appended to $HOME/.ssh/config (the file is newly created if no exist). This is like an Azure version of [ec2ssh](https://github.com/mirakui/ec2ssh) or [aws-ssh-config](https://github.com/gianlucaborello/aws-ssh-config) that strongly inspired this initiative. This would be very helpful when you manage lots of VMs that have dynamic IP assignment settings and need frequent VM up-and-down operations for them which causes the change of IPs assigned to VMs. In such a case, azure-ssh-config will definitly make your SSH life easy.


## Installation

To run azure-ssh-config, [azura](https://pypi.python.org/pypi/azure), [msrestazure](https://pypi.python.org/pypi/msrestazure), and [simplejson](https://pypi.python.org/pypi/simplejson/) python packages need to be installed.

```
pip install simplejson
pip install --pre azure --upgrade
pip install msrestazure
```

Get azure-ssh-config script copy from github and see if all required packages are installed

```
git clone git@github.com:yokawasa/azure-ssh-config.git
cd azure-ssh-config
azure-ssh-config.py --version
```

## Configuration

Generate client profile template by executing the following command.

```
azure-ssh-config.py --init
```

Configure client profile file

```
vi $HOME/.azure/azure-ssh-config.json

{
    "subscription_id": "<YOUR SUBSCRIPTION ID>",
    "client_id": "<YOUR APPLICATION CLIENT IP>",
    "client_scret": "<YOUR APPLICATION CLIENT SCRET>",
    "tenant_id": "<YOUR TENANT ID>"
}
```


## Usage

Assuming all required packages are installed and rightly configured, you're ready to run azure-ssh-config

```
python azure-ssh-config.py --help

usage: azure-ssh-config.py [-h] [--version] [--init] [--profile PROFILE]
                           [--user USER] [--identityfile IDENTITYFILE]
                           [--private] [--resourcegroups RESOURCEGROUPS]

This program generates SSH config from Azure ARM VM inventry in subscription

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --init                Create template client profile at $HOME/.azure/azure-
                        ssh-config.json only if there is no existing one
  --profile PROFILE     Specify azure client profile file to use ($HOME/.azure
                        /azure-ssh-config.json by default)
  --user USER           SSH username to use for all hosts
  --identityfile IDENTITYFILE
                        SSH identity file to use for all hosts
  --private             Use private IP addresses (Public IP is used by
                        default)
  --resourcegroups RESOURCEGROUPS
                        A comma-separated list of resource group to be
                        considered for ssh-config generation (all resource
                        groups by default)
```


### 1. Running with no optional args
```
azure-ssh-config.py
```

Each host entry in output ssh-config file is simple like this:

```
cat ~/.ssh/config

### AZURE-SSH-CONFIG BEGIN ###

Host myvm1
    HostName 40.74.124.30

Host myvm2
    HostName 40.74.116.134
....

### AZURE-SSH-CONFIG END ###
```


### 2. Running with user and identity file options
```
azure-ssh-config.py --user yoichika --identityfile ~/.ssh/id_rsa
```

User and identify file are added to each host entry in output ssh-config file:

```
cat ~/.ssh/config

### AZURE-SSH-CONFIG BEGIN ###

Host myvm1
    HostName 40.74.124.30
    IdentityFile /home/yoichika/.ssh/id_rsa
    User yoichika

Host myvm2
    HostName 40.74.116.134
    IdentityFile /home/yoichika/.ssh/id_rsa
    User yoichika
....

### AZURE-SSH-CONFIG END ###
```

### 3. Running with user, identity file, and resource group options
```
azure-ssh-config.py --user yoichika \
                --identityfile ~/.ssh/id_rsa \
                --resourcegroups mygroup1,mygroup2
```

Only host entry that belong to specified resource group are added in ssh-config


## TODO

* Python Packaging
* Support bash/zsh Completion


## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/yokawasa/azure-ssh-config.

## Copyright

<table>
  <tr>
    <td>Copyright</td><td>Copyright (c) 2016- Yoichi Kawasaki</td>
  </tr>
  <tr>
    <td>License</td><td>MIT</td>
  </tr>
</table>

