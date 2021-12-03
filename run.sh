#!/bin/bash

./connect.sh
export ANSIBLE_NAME_CONTAINS=master
python3 create_vm.py
ansible all -i orka_inventory.py -m ping # TODO: get real playbook for Jenkins master install
export ANSIBLE_NAME_CONTAINS=agent
python3 create_vm.py
ansible all -i orka_inventory.py -m ping # TODO: get real playbook for Jenkins agent install
python3 save_and_cleanup.py
