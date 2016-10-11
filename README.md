# Azure SSH Config (azuresshconfig)

Generate SSH config file from Azure ARM VM inventry in subscription

## Introduction

azuresshconfig is a simple script that collects Azure ARM Virtual Machine(VM) inventry in subscription and generate a SSH config entries to be appended to $HOME/.ssh/config (the file is newly created if no exist). This is like an Azure version of [ec2ssh](https://github.com/mirakui/ec2ssh) or [aws-ssh-config](https://github.com/gianlucaborello/aws-ssh-config) that strongly inspired this initiative. This would be very helpful when you manage lots of VMs that have dynamic IP assignment settings and need frequent VM up-and-down operations for them which causes the change of IPs assigned to VMs. In such a case, azuresshconfig will definitly make your SSH life easy.


## Installation

```
pip install azuresshconfig
```

## Configuration

Generate client profile template file by executing the following command.

```
azuresshconfig --init
```

Configure the client profile file 

```
vi $HOME/.azure/azuresshconfig.json

{
    "subscription_id": "<YOUR SUBSCRIPTION ID>",
    "client_id": "<YOUR APPLICATION CLIENT IP>",
    "client_scret": "<YOUR APPLICATION CLIENT SCRET>",
    "tenant_id": "<YOUR TENANT ID>"
}
```

As you can see, you need to create a service principal to fill out the parameters above. For those who don't know how to create service principal, there is a great instruction: [Use Azure CLI to create a service principal to access resources](https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal-cli/)


## Usage

Assuming all required packages are installed and rightly configured, you're ready to run azuresshconfig

```
azuresshconfig --help

usage: azuresshconfig [-h] [--version] [--init] [--profile PROFILE]
                           [--user USER] [--identityfile IDENTITYFILE]
                           [--private] [--resourcegroups RESOURCEGROUPS]

This program generates SSH config from Azure ARM VM inventry in subscription

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --init                Create template client profile at $HOME/.azure/azure-
                        ssh-config.json only if there is no existing one
  --profile PROFILE     Specify azure client profile file to use ($HOME/.azure
                        /azuresshconfig.json by default)
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
azuresshconfig
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
azuresshconfig --user yoichika --identityfile ~/.ssh/id_rsa
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
azuresshconfig --user yoichika \
                --identityfile ~/.ssh/id_rsa \
                --resourcegroups mygroup1,mygroup2
```

Only host entry that belong to specified resource group are added in ssh-config

## Todo

* Support bash/zsh Completion

## Issues

* [Kown Issues and resolutions](Issues.md)
* [Current Issues, bugs, and requests](https://github.com/yokawasa/azure-ssh-config/issues)

## Change log

* [Changelog](ChangeLog.md)

## Links

* https://pypi.python.org/pypi/azuresshconfig/

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

