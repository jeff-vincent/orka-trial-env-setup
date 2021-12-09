#!/bin/bash

./connect.sh
python3 create_vm.py --vm_name "master"
python3 orka_inventory.py --host "master"
ansible all -i inventory -m ping # TODO: get real playbook for Jenkins master install
python3 create_vm.py --vm_name "agent"
python3 orka_inventory.py --host "agent"
ansible all -i inventory -m ping # TODO: get real playbook for Jenkins agent install
python3 save_and_cleanup.py
