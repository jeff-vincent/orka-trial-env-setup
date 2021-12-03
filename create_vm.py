import json
import os
import random
import requests
import string
import time

class SpinUpOrkaVM:
	def __init__(self):
		self.token = None
		self.vm_name = os.environ['ANSIBLE_NAME_CONTAINS']
		self.orka_address = 'http://10.221.188.100'
		self.orka_user = os.environ['ORKA_USER']
		self.orka_pass = os.environ['ORKA_PASS']
		self.core_count = os.environ['CORE_COUNT']
		self.vcpu_count = os.environ['VCPU_COUNT']

	def get_auth_token(self):
		data = {'email': self.orka_user, 'password': self.orka_pass}
		result = requests.post(self.orka_address+'/token', data=data)
		content = json.loads(result._content.decode('utf-8'))
		self.token = content['token']

	def create_vm_config(self):
		orka_address = f"{self.orka_address}/resources/vm/create"
		headers = {
			'Content-Type': 'application/json', 
			'Authorization': f"Bearer {self.token}"
			}
		data = {
			'orka_vm_name': self.vm_name,
			'orka_base_image': self.orka_base_image,
			'orka_image': self.vm_name,
			'orka_cpu_core': int(self.core_count),
			'vcpu_count': int(self.vcpu_count)
			}
		requests.post(orka_address, data=json.dumps(data), headers=headers)
        
	def deploy_vm_config(self):
		orka_address = f"{self.orka_address}/resources/vm/deploy"
		headers = {'Content-Type': 'application/json', 'Authorization': f"Bearer {self.token}"}
		data =  {'orka_vm_name': self.vm_name}
		result = requests.post(orka_address, data=json.dumps(data), headers=headers)
		content = json.loads(result._content.decode('utf-8'))
		self.vm_ip = content['ip']
		self.vm_ssh_port = content['ssh_port']

	# def revoke_orka_auth_token(self):
	# 	url = f"{self.orka_address}/token"
	# 	headers = {
 #            	'Content-Type': 'application/json',
 #            	'Authorization': f"Bearer {self.token}"
 #            	}
	# 	requests.delete(url, headers=headers)


def main(spin_up):
	spin_up.get_auth_token()
	spin_up.create_vm_config()
	spin_up.deploy_vm_config()
	
if __name__ == '__main__':
	spin_up = SpinUpOrkaVM()
	main(spin_up)
