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

Configure the client profile file, in which you add your service principal account info to access your resources in Azure via Azure APIs.

```
vi $HOME/.azure/azuresshconfig.json

{
    "subscription_id": "<YOUR SUBSCRIPTION ID>",
    "client_id": "<YOUR APPLICATION CLIENT IP>",
    "client_scret": "<YOUR APPLICATION CLIENT SCRET>",
    "tenant_id": "<YOUR TENANT ID>"
}
```

For those who don't know how to create service principal, there is a great instruction: [Use Azure CLI to create a service principal to access resources](https://azure.microsoft.com/en-us/documentation/articles/resource-group-authenticate-service-principal-cli/). If you have Azure CLI 2.0 command installed on your evironment, you can create your service principal and configure its access to your azure resources with a single command 'az ad sp create-for-rbac'. 

Suppose your app id uri is 'http://unofficialism.info' and role you want to give for the app is 'Reader', you can create your service principal like this:

```
az ad sp create-for-rbac -n "http://unofficialism.info" --role reader

```

You will get an output like this, and with them you can fill out the client profile file:

```
{
  "appId": "c36x4b4f-bef6-422e-bd3b-65057e7ab065",        # -> client_id in client profile file
  "displayName": "azure-cli-2017-03-30-05-16-59",         
  "name": "http://unofficialism.info",
  "password": "32126d32-7453-4053-3353-c420d4ffef2e",     # -> client_scret in client profile file
  "tenant": "72f988bf-86f1-41af-91cb-2d7cd011db47"        # -> tenant_id in client profile file
}
```

For the detail of service principal role, please refer to [Built-in roles for Azure Role-Based Access Control](https://docs.microsoft.com/en-us/azure/active-directory/role-based-access-built-in-roles).


## Usage

Assuming all required packages are installed and rightly configured, you're ready to run azuresshconfig

```
azuresshconfig --help

usage: azuresshconfig.py [-h] [--version] [--init] [--profile PROFILE]
                         [--output OUTPUT] [--user USER]
                         [--identityfile IDENTITYFILE] [--private]
                         [--resourcegroups RESOURCEGROUPS] [--params PARAMS]

This program generates SSH config from Azure ARM VM inventry in subscription

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --init                Create template client profile at
                        $HOME/.azure/azuresshconfig.json only if there is no
                        existing one
  --profile PROFILE     Specify azure client profile file to use
                        ($HOME/.azure/azuresshconfig.json by default)
  --output OUTPUT       Specify ssh config file path ($HOME/.ssh/config by
                        default). Or specify "stdout" if you want to print its
                        output to STDOUT
  --user USER           SSH username to use for all hosts
  --identityfile IDENTITYFILE
                        SSH identity file to use for all hosts
  --private             Use private IP addresses (Public IP is used by
                        default)
  --resourcegroups RESOURCEGROUPS
                        A comma-separated list of resource group to be
                        considered for ssh-config generation (all resource
                        groups by default)
  --params PARAMS       Any ssh-config params you want to add with query-
                        string format: key1=value1&key2=value2&...
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


### 2. Running with user, output, and identity file options
```
azuresshconfig --user yoichika --output /mypath/config --identityfile ~/.ssh/id_rsa
```

User and identify file are added to each host entry in output ssh-config file:

```
cat /mypath/config

### AZURE-SSH-CONFIG BEGIN ###

Host myvm1
    HostName 40.74.124.30
    IdentityFile ~/.ssh/id_rsa
    User yoichika

Host myvm2
    HostName 40.74.116.134
    IdentityFile ~/.ssh/id_rsa
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

### 4. Running with user, identity file, and additional ssh-config params
```
azuresshconfig.py --user yoichika \
                --identityfile ~/.ssh/id_rsa \
                --params "Port=2222&Protocol=2&UserKnownHostsFile=~/.ssh/known_hosts&ForwardAgent=yes"
```

Additional ssh-config params specified by --params are added to an output ssh-config file like this:

```
cat ~/.ssh/config

### AZURE-SSH-CONFIG BEGIN ###

Host myvm1
    HostName 40.74.124.30
    IdentityFile ~/.ssh/id_rsa
    User yoichika
    Port 2222
    Protocol 2
    UserKnownHostsFile ~/.ssh/known_hosts
    ForwardAgent yes

Host myvm2
    HostName 40.74.116.134
    IdentityFile /home/yoichika/.ssh/id_rsa
    User yoichika
    Port 2222
    Protocol 2
    UserKnownHostsFile ~/.ssh/known_hosts
    ForwardAgent yes
....

### AZURE-SSH-CONFIG END ###
```

## Docker (Dockerfile)

Now docker image for azuresshconfig is available (yoichikawasaki/azuresshconfig). The image is based on Alpine Linux image, and contains Python2.7, pip, azuresshconfig Python packages and its prerequisite libraries.

Download size of this image is only 155 MB
```
$ docker images azuresshconfig
REPOSITORY                          TAG                 IMAGE ID            CREATED             SIZE
azuresshconfig                     latest              7488bef4343f        7 minutes ago       155 MB
```

### Usage Example

```bash
$ docker run -v $HOME/.azure:/root/tmp \
    --rm -it yoichikawasaki/azuresshconfig \
    --profile /root/tmp/azuresshconfig.json --output stdout \
    --user yoichika --identityfile ~/.ssh/id_rsa > $HOME/.ssh/config
```
or you can build from Dockerfile and run your local images like this:

```bash
$ docker build -t azuresshconfig .
$ docker run -v $HOME/.azure:/root/tmp \
    --rm -it azuresshconfig \
    --profile /root/tmp/azuresshconfig.json --output stdout \
    --user yoichika --identityfile ~/.ssh/id_rsa > $HOME/.ssh/config
```

## Shell Completion
### Bash
Bash completion will work by loading bash/[azuresshconfig_completion.bash](https://github.com/yokawasa/azure-ssh-config/blob/master/bash/azuresshconfig_completion.bash). In order to load azuresshconfig_completion.bash, you can do like this
```
# copy this under either of following directories
cp azuresshconfig_completion.bash (/etc/bash_completion.d | /usr/local/etc/bash_completion.d | ~/bash_completion.d)

# or append 'source /path/to/azuresshconfig_completion.bash' to .bashrc like this
echo 'source /path/to/azuresshconfig_completion.bash' >> .bashrc
```

Once azuresshconfig_completion.bash is loaded, Bash completion will work this:
```
$ azuresshconfig -[tab]
-h                --identityfile    --params          --profile         --user
--help            --init            --private         --resourcegroups

$ azuresshconfig --i[tab]
--identityfile  --init

$ azuresshconfig --p[tab]
--params   --private  --profile

$ azuresshconfig --user [tab]
$ azuresshconfig --user <ssh_user>
$ azuresshconfig --user <ssh_user> --identityfile [tab]
$ azuresshconfig --user <ssh_user> --identityfile <ssh_identity_file>
```

## Todo

* Support zsh Completion (Hopefully support it soon)

## Issues

* [Kown Issues and resolutions](Issues.md)
* [Current Issues, bugs, and requests](https://github.com/yokawasa/azure-ssh-config/issues)

## Change log

* [Changelog](ChangeLog.md)

## Links

* https://pypi.python.org/pypi/azuresshconfig/
* http://unofficialism.info/posts/azuresshconfig/

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

