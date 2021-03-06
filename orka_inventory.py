#!/usr/local/bin/python3

import argparse
import json
import os
import requests
import subprocess
from create_vm import SpinUpOrkaVM

class OrkaAnsibleInventory:

    def __init__(self):
        self.spin_up = SpinUpOrkaVM()
        self.orka_user = os.environ.get('ORKA_USER')
        self.orka_license_key = os.environ.get('ORKA_LICENSE_KEY')
        self.vm_data = None
        self.filtered_data = None
        self.inventory_header = ('[all:vars]\nanisble_connection=ssh\n'
                        'ansible_ssh_user=admin\n'
                        'ansible_ssh_pass=admin\n'
                        'ansible_ssh_common_args ="-o ConnectionAttempts=20"\n\n'
                        '[hosts]\n')
        # self.inventory = {
        #     'group': {'hosts': []},
        #     'vars': [],
        #     '_meta': {
        #         'hostvars': {}
        #     }
        # }

    # def get_current_vm_data(self):
    #     """Get current VM data related to the current CLI user.
    #     Note
    #     ----
    #     The user must be logged in to the Orka CLI.
    #     """
    #     completed_process = subprocess.run(
    #         ['orka', 'vm', 'list', '--json'], 
    #         capture_output=True)
    #     dict_string = completed_process.stdout.decode('utf-8')
    #     data = json.loads(dict_string)
    #     self.vm_data = data['virtual_machine_resources']

    def get_current_vm_data(self):
        self.spin_up.get_auth_token()
        token = self.spin_up.token
        headers = {
		    'Content-Type': 'application/json', 
		    'Authorization': f"Bearer {token}",
            'orka-licensekey': self.orka_license_key
	    }
        r = requests.get(f"http://10.221.188.100/resources/vm/list/{self.orka_user}", headers=headers)
        data = r.json()
        self.vm_data = data['virtual_machine_resources']
        # self.spin_up.revoke_orka_auth_token()

    def get_deployed_vms(self):
        """Filter current VM data to isolate deployed VMs."""
        self.filtered_data = \
            [i for i in self.vm_data if i['vm_deployment_status'] == 'Deployed']

    def get_vm_by_host_name(self, host_name):
        """Filter current VM data to isolate named VM.
        Args:
            host_name: string: the VM name to match.
        """
        self.filtered_data = \
            [i for i in self.vm_data if host_name == i['status'][0]['virtual_machine_name']]

    def get_name_contains_vms(self, name_contains):
        """Filter current VM data to isolate VMs by partial name match.
        Args:
            name_contains: string: partial match sort key for deployed VMs.
        """
        nc = name_contains.lower()
        self.filtered_data = \
            [i for i in self.filtered_data if nc in i['status'][0]['virtual_machine_name'].lower()]

    # def _build_vars(self):
    #     """Build the vars dict to pass to Ansible"""
    #     ansible_ssh_user = os.environ.get('ANSIBLE_SSH_USER')
    #     ansible_ssh_pass = os.environ.get('ANSIBLE_SSH_PASS')
    #     ansible_connection = 'ssh'

    #     return {
    #         'ansible_connection': ansible_connection,
    #         'ansible_ssh_user': ansible_ssh_user,
    #         'ansible_ssh_pass': ansible_ssh_pass
    #     }

    # def create_inventory(self):
    #     """Create the inventory object to return to Ansible."""
    #     hosts = []
    #     ansible_ssh_user = 'admin'
    #     ansible_ssh_pass = 'admin'

    #     for i in self.filtered_data:
    #         ip_address = i['status'][0]['virtual_machine_ip']
    #         hosts.append(ip_address)
    #         self.inventory['_meta']['hostvars'][ip_address] = \
    #             {'ansible_ssh_port': i['status'][0]['ssh_port'],
    #             'ansible_ssh_user': ansible_ssh_user,
    #             'ansible_ssh_pass': ansible_ssh_pass,
    #             'ansible_connection': 'ssh'}

    #     self.inventory['group']['hosts'] = hosts
    #     # varss = self._build_vars()
    #     # self.inventory['vars'] = varss
    #     print(json.dumps(self.inventory))
    #     return json.dumps(self.inventory)

    def write_inventory(self):
        """Write current VM data -- sorted or not -- to an 
        Ansible inventory file.
        
        Parameters
        ----------
        
        data: list
            A list of Python dicts that represent Orka VMs.
        """
        with open('inventory', 'w+') as f:
            f.write(self.inventory_header)
            for i in self.filtered_data:
                line = '{}   ansible_ssh_port={}   ansible_ssh_host={}'.format(
                    i['virtual_machine_name'],
                    i['status'][0]['ssh_port'],
                    i['status'][0]['virtual_machine_ip'])
                f.write(line + '\n')


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list', help='list deployed VMs',
                    action='store_true')
    group.add_argument('--host', help='get host by name', action='store',
                    dest='host_name')
    return parser.parse_args()


def main(args, name_contains):
    if args.host_name:
        host_name = args.host_name
        inventory_creator = OrkaAnsibleInventory()
        inventory_creator.get_current_vm_data()
        inventory_creator.get_vm_by_host_name(host_name)
        inventory_creator.write_inventory()
    elif args.list:
        inventory_creator = OrkaAnsibleInventory()
        inventory_creator.get_current_vm_data()
        inventory_creator.get_deployed_vms()
        if name_contains:
            inventory_creator.get_name_contains_vms(name_contains)
        inventory_creator.write_inventory()
    else:
        print('Warning: you must pass either `--list` or `--host <hostname>` argument.')


if __name__ == '__main__':
    args = parse_args()
    name_contains = os.environ.get('ANSIBLE_NAME_CONTAINS')
    main(args, name_contains)
    
