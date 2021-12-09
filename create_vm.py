import argparse
import json
import os
import requests

class SpinUpOrkaVM():

	def __init__(self):
		self.token = None
		self.orka_address = 'http://10.221.188.100'
		self.orka_user = os.environ['ORKA_USER']
		self.orka_pass = os.environ['ORKA_PASS']
		self.core_count = os.environ['CORE_COUNT']
		self.vcpu_count = os.environ['VCPU_COUNT']
		self.orka_base_image = '90GBigSurSSH.img'

	def get_auth_token(self):
		data = {'email': self.orka_user, 'password': self.orka_pass}
		result = requests.post(f"{self.orka_address}/token", data=data)
		content = json.loads(result._content.decode('utf-8'))
		self.token = content['token']

	def create_vm_config(self, vm_name):
		orka_address = f"{self.orka_address}/resources/vm/create"
		headers = {
			'Content-Type': 'application/json', 
			'Authorization': f"Bearer {self.token}"
		}
		data = {
			'orka_vm_name': vm_name,
			'orka_base_image': self.orka_base_image,
			'orka_image': vm_name,
			'orka_cpu_core': int(self.core_count),
			'vcpu_count': int(self.vcpu_count)
		}
		requests.post(orka_address, data=json.dumps(data), headers=headers)
        
	def deploy_vm_config(self, vm_name):
		orka_address = f"{self.orka_address}/resources/vm/deploy"
		headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {self.token}"}
		data =  {'orka_vm_name': vm_name}
		result = requests.post(orka_address, data=json.dumps(data), headers=headers)
		content = json.loads(result._content.decode('utf-8'))
		self.vm_ip = content['ip']
		self.vm_ssh_port = content['ssh_port']

	def revoke_orka_auth_token(self):
		url = f"{self.orka_address}/token"
		headers = {
            		'Content-Type': 'application/json',
            		'Authorization': f"Bearer {self.token}"
        	}
		requests.delete(url, headers=headers)


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--vm_name', dest='vm_name', action='store')
	return parser.parse_args()


def main(args, spin_up):
	spin_up.get_auth_token()
	spin_up.create_vm_config(args.vm_name)
	spin_up.deploy_vm_config(args.vm_name)
	# spin_up.revoke_orka_auth_token()
	

if __name__ == '__main__':
	args = parse_args()
	spin_up = SpinUpOrkaVM()
	main(args, spin_up)
