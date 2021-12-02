#!/bin/bash

./connect.sh 
python3 create_vms.py
ansible all -i orka_inventory.py -m ping # TODO: get real playbook for Jenkins install
python3 save_and_cleanup.py