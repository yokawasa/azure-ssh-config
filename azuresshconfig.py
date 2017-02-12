#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Yoichi Kawasaki'

import sys
import os
import argparse
import simplejson as json

try:
    from msrestazure.azure_active_directory import ServicePrincipalCredentials
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.network import NetworkManagementClient
    from azure.mgmt.network.models.public_ip_address_dns_settings import PublicIPAddressDnsSettings
except ImportError:
    pass

### Global Defines
_AZURE_SSH_CONFIG_VERSION = '0.2.1'
_AZURE_SSH_CONFIG_HOME_SITE = 'https://github.com/yokawasa/azure-ssh-config'
_DEFAULT_AZURE_SSH_CONFIG_JSON_FILE = '{}/.azure/azuresshconfig.json'.format(os.environ['HOME'])
_DEFAULT_SSH_CONFIG_FILE = '{}/.ssh/config'.format(os.environ['HOME'])
_DEFAULT_SSH_CONFIG_BLOCK_START_MAKR = "### AZURE-SSH-CONFIG BEGIN ###"
_DEFAULT_SSH_CONFIG_BLOCK_END_MARK = "### AZURE-SSH-CONFIG END ###"


class SSHConfigBlock:
    def __init__(self):
        self._entries = []
        # definitions below are collected from man ssh_config(5) 
        self._ssh_config_param_defines = ['Host', 'AddressFamily', 'BatchMode', 'BindAddress', 'ChallengeResponseAuthentication', 'CheckHostIP', 'Cipher', 'Ciphers', 'ClearAllForwardings', 'Compression', 'CompressionLevel', 'ConnectionAttempts', 'ConnectTimeout', 'ControlMaster', 'ControlPath', 'ControlPersist', 'DynamicForward', 'EnableSSHKeysign', 'EscapeChar', 'ExitOnForwardFailure', 'ForwardAgent', 'ForwardX11', 'ForwardX11Timeout', 'ForwardX11Trusted', 'GatewayPorts', 'GlobalKnownHostsFile', 'GSSAPIAuthentication', 'GSSAPIDelegateCredentials', 'HashKnownHosts', 'HostbasedAuthentication', 'HostKeyAlgorithms', 'HostKeyAlias', 'HostName', 'IdentitiesOnly', 'IdentityFile', 'IgnoreUnknown', 'IPQoS', 'KbdInteractiveAuthentication', 'KbdInteractiveDevices', 'KexAlgorithms', 'LocalCommand', 'LocalForward', 'LogLevel', 'MACs', 'NoHostAuthenticationForLocalhost', 'NumberOfPasswordPrompts', 'PasswordAuthentication', 'PermitLocalCommand', 'PKCS11Provider', 'Port', 'PreferredAuthentications', 'Protocol', 'ProxyCommand', 'PubkeyAuthentication', 'RekeyLimit', 'RemoteForward', 'RequestTTY', 'RhostsRSAAuthentication', 'RSAAuthentication', 'SendEnv', 'ServerAliveCountMax', 'ServerAliveInterval', 'StrictHostKeyChecking', 'TCPKeepAlive', 'Tunnel', 'TunnelDevice', 'UsePrivilegedPort', 'User', 'UserKnownHostsFile', 'VerifyHostKeyDNS', 'VersionAddendum', 'VisualHostKey', 'XAuthLocation' ]

    def add_entry(self,entry_name, access_address, params ):
        entry = {
           'Name' :  entry_name,
           'HostName': access_address
        }
        for d in self._ssh_config_param_defines:
            if exists_in_dict(d, params):
                entry[d] = params[d]
        self._entries.append(entry)

    def to_string(self):
        buffer = ''
        for entry in self._entries:
            buffer += "Host {}\n".format(entry['Name'])
            buffer += "    HostName {}\n".format(entry['HostName'])
            for d in self._ssh_config_param_defines:
                if exists_in_dict(d, entry):
                    buffer += "    {0} {1}\n".format(d, entry[d])
            buffer += "\n"
        return buffer

class SSHConfig:
    def __init__(self, sshconfig=_DEFAULT_SSH_CONFIG_FILE,
            block_start_mark=_DEFAULT_SSH_CONFIG_BLOCK_START_MAKR, 
            block_end_mark=_DEFAULT_SSH_CONFIG_BLOCK_END_MARK ):
        self.sshconfig = sshconfig
        self._block_start_mark = "{}\n".format(block_start_mark)
        self._block_end_mark  = "{}\n".format(block_end_mark)
        self._block = ''
        self._pre_block = ''
        self._post_block = ''
        self.__prepare()
        self.__parse()

    def __prepare(self):
        if not os.path.exists(self.sshconfig):
            # Create an Empty SSH Config file
            open(self.sshconfig, 'a').close()

    def __parse(self):
        try:
            f = open(self.sshconfig, "r")
            contents = f.read()
            start_block_mark_startpos = contents.find(self._block_start_mark)
            if (start_block_mark_startpos > -1):
                block_startpos = start_block_mark_startpos + len(self._block_start_mark)
                block_endpos = contents.find(self._block_end_mark, block_startpos)
                if (block_endpos > -1):
                    end_block_mark_endpos = block_endpos + len(self._block_end_mark)
                    self._block  = contents[block_startpos:block_endpos]
                    self._pre_block = contents[:start_block_mark_startpos]
                    self._post_block = contents[end_block_mark_endpos:]
                else:
                    print_err("You have start block mark but not end mark!")
                    raise Exception("Unexpected error: invlid block mark: {0}".format(self.sshconfig))
            else:
                self._pre_block = contents
        except IOError:
            print_err('Cannot Open %s' % self.sshconfig )
            raise
        else:
            f.close()
        
    def block_exists(self):
        return True if self._block else False

    def get_block (self):
        return self._block

    def append_block (self,block):
        self._block = block
        try:
            f = open(self.sshconfig,"w")
            f.write( "{0}{1}{2}\n{3}".format(
                self._pre_block,
                self._block_start_mark,
                block,
                self._block_end_mark))
        except IOError:
            print_err('Cannot Open %s' % self.sshconfig )
            raise
        else:
            f.close
       
    def update_block (self, block):
        self._block = block
        try:
            f = open(self.sshconfig,"w")
            f.write( "{0}{1}{2}\n{3}{4}".format(
                self._pre_block,
                self._block_start_mark,
                block,
                self._block_end_mark,
                self._post_block))
        except IOError:
            print_err('Cannot Open {}'.format(self.sshconfig) )
            raise
        else:
            f.close


class ClientProfileConfig:
    def __init__(self,config_file):
        self.subscription_id = ''
        self.client_id = ''
        self.client_scret = ''
        self.tenant_id = ''
        self.__open_read_config(config_file)

    def __open_read_config(self,config_file):
        try:
            cf = open(config_file, 'r')
            o = json.load(cf)
            self.subscription_id= str(o['subscription_id'])
            self.client_id = str(o['client_id'])
            self.client_scret = str(o['client_scret'])
            self.tenant_id = str(o['tenant_id'])
        except IOError:
            print_err('Cannot Open {}'.format(config_file) )
        else:
            cf.close()

    def dump(self):
        print("Azure SSH config client profile dump:\n\tsubscription_id={0}\n"
              "\tclient_id={1}\n\tclient_scret={2}\n\ttenant_id={3}".format(
             self.subscription_id, self.client_id, self.client_scret, self.tenant_id))

    @staticmethod
    def generate_template(any_file):
        try:
            f = open(any_file,"w")
            f.write(
                "{\n"
                "    \"subscription_id\": \"<YOUR SUBSCRIPTION ID>\",\n"
                "    \"client_id\": \"<YOUR APPLICATION CLIENT IP>\",\n"
                "    \"client_scret\": \"<YOUR APPLICATION CLIENT SCRET>\",\n"
                "    \"tenant_id\": \"<YOUR TENANT ID>\"\n"
                "}"
                )
        except IOError:
            print_err('Cannot Open {}'.format(any_file) )
        else:
            f.close


def print_err(s):
    sys.stderr.write("[ERROR] {}\n".format(s))

def exists_in_list (elem, target_list):
    return elem in target_list

def exists_in_dict (key, target_dict):
    return True if ( target_dict.has_key(key) and target_dict[key] ) else False

def get_resorucegroup_from_vmid (vmid):
    ids = vmid.split('/')
    # virutal machine id format:
    #   /subscriptions/<s>/resourceGroups/<s>/providers/<s>/virtualMachines/<s>
    if len(ids) != 9:
        pass
    return ids[4]


def get_network_interface_info (network_client, network_interface_id):
    ni_info = {}
    ids = network_interface_id.split('/')
    # network interface id format:
    #   /subscriptions/<s>/resourceGroups/<s>/providers/<s>/networkInterfaces/<s>
    if len(ids) != 9:
        pass
    ni =  network_client.network_interfaces.get( ids[4], ids[8] )
    ipconfigs= ni.ip_configurations
    ipconfig = ipconfigs[0]
    # privte ip
    ni_info['private_ip'] = ipconfig.private_ip_address
    # get public address
    if not ipconfig.public_ip_address:
        return ni_info
    public_address_id = ipconfig.public_ip_address.id
    # public address id format:
    #   /subscriptions/<s>/resourceGroups/<s>/providers/<s>/publicIPAddresses/<s>
    pas= public_address_id.split('/')
    if len(pas) != 9:
        return ni_info
    pia = network_client.public_ip_addresses.get(pas[4], pas[8])
    if pia.dns_settings:
        dns_settings = pia.dns_settings
        if dns_settings.domain_name_label and dns_settings.fqdn:
            ni_info['fqdn']  = dns_settings.fqdn
    if pia.ip_address:
        ni_info['public_ip'] = pia.ip_address
    return ni_info


def main():
    parser = argparse.ArgumentParser(description='This program generates SSH config from Azure ARM VM inventry in subscription')
    parser.add_argument(
        '--version', action='version', version=_AZURE_SSH_CONFIG_VERSION)
    parser.add_argument(
        '--init', action='store_true',
        help='Create template client profile at $HOME/.azure/azuresshconfig.json only if there is no existing one')
    parser.add_argument(
        '--profile',
        help='Specify azure client profile file to use ($HOME/.azure/azuresshconfig.json by default)')
    parser.add_argument(
        '--user',
        help='SSH username to use for all hosts')
    parser.add_argument(
        '--identityfile',
        help='SSH identity file to use for all hosts')
    parser.add_argument(
        '--private', action='store_true',
        help='Use private IP addresses (Public IP is used by default)')
    parser.add_argument(
        '--resourcegroups',
        help='A comma-separated list of resource group to be considered for ssh-config generation (all resource groups by default)')
    parser.add_argument(
        '--params',
        help='Any ssh-config params you want to add with query-string format: key1=value1&key2=value2&...')
    args = parser.parse_args()

    if args.init:
        # check if $HOME/.azure directory exists and create if not exists
        azure_config_home = '{}/.azure'.format(os.environ['HOME'])
        if not os.path.exists(azure_config_home):
            os.makedirs(azure_config_home)

        # Initialize azure client profile file
        if not os.path.exists(_DEFAULT_AZURE_SSH_CONFIG_JSON_FILE):
            ClientProfileConfig.generate_template(_DEFAULT_AZURE_SSH_CONFIG_JSON_FILE)   
            print ("Created template client profile!: {}".format(
                        _DEFAULT_AZURE_SSH_CONFIG_JSON_FILE))
        else:
            print_err("No action has done since client profile file already exist!: {}".format(
                        _DEFAULT_AZURE_SSH_CONFIG_JSON_FILE))
        quit()
            
    ### Args Validation
    client_profile_file = args.profile if args.profile else _DEFAULT_AZURE_SSH_CONFIG_JSON_FILE
    if not os.path.exists(client_profile_file):
        print_err("Client profile doesn't exist: {0}\n"
                  "For the client profile detail, refer to {1}".format(
                    client_profile_file, _AZURE_SSH_CONFIG_HOME_SITE))
        quit()

    ssh_default_user = args.user if args.user else ''
    ssh_default_identityfile = args.identityfile if args.identityfile else ''
    option_private_ip = args.private
    filter_resource_groups = []
    if args.resourcegroups:
        lower_rg = args.resourcegroups.lower()
        rslist= lower_rg.split(',')
        if len(rslist) > 0:
            filter_resource_groups = rslist
    additional_params = []
    if args.params:
        pairlist = args.params.split('&')
        for s in pairlist:
            p = s.split('=')
            if (len(p)==2):
                additional_params.append(p)

    ### Load Config 
    cconf = ClientProfileConfig(client_profile_file)
    
    ### Get Target virtual machines info List
    credentials = ServicePrincipalCredentials(
                    cconf.client_id,cconf.client_scret,
                    tenant=cconf.tenant_id)
    compute_client = ComputeManagementClient(
                    credentials, cconf.subscription_id)
    network_client = NetworkManagementClient(
                    credentials, cconf.subscription_id)
    target_vm_list = []
    for vm in compute_client.virtual_machines.list_all():
        target_vm = {}
        target_vm['name'] = vm.name
        vm_rgroup = get_resorucegroup_from_vmid(vm.id)
        # Filtering by resource group if needed
        if len(filter_resource_groups) > 0:
            r = vm_rgroup.lower()
            if not exists_in_list(r, filter_resource_groups ):
                continue  # skip
        network_interfaces = vm.network_profile.network_interfaces
        for ni in network_interfaces:
            ni_info = get_network_interface_info(network_client, ni.id)
            if option_private_ip:
                if exists_in_dict('private_ip',ni_info):
                    target_vm['access_ip'] = ni_info['private_ip'] 
            else:
                if exists_in_dict('public_ip',ni_info):
                    target_vm['access_ip'] = ni_info['public_ip'] 
            if exists_in_dict('access_ip',target_vm):
                break
        # Add only vm that has access_ip
        if exists_in_dict('access_ip',target_vm):
            target_vm_list.append(target_vm)

    ### Generate and append config block to ssh-config file
    scblock = SSHConfigBlock()
    for v in target_vm_list:
        params = {}
        if ssh_default_user:
            params['User'] = ssh_default_user
        if ssh_default_identityfile:
            params['IdentityFile'] = ssh_default_identityfile
        if len(additional_params) > 0:
            for pset in additional_params:
                params[pset[0]] = pset[1]
        scblock.add_entry(v['name'], v['access_ip'],params)
    ssh_config_block = scblock.to_string()

    ssh_config = SSHConfig()
    if ssh_config.block_exists():
        ssh_config.update_block(ssh_config_block)
    else:
        ssh_config.append_block(ssh_config_block)

    print "Done! Updated: {}".format(ssh_config.sshconfig)

if __name__ == "__main__":
    main()

#
# vim:ts=4 et
#
