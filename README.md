# orka-trial-env-setup

Set up a Jenkins master and create an associated agent image in Orka by running the following:

```
git clone https://github.com/jeff-vincent/orka-trial-env-setup.git
cd orka-trial-env-setup
sudo docker build -t trial_env .
```
```
sudo docker run --privileged --name orka_env \
-e ORKA_USER=<YOUR_EMAIL> \
-e ORKA_PASS=<YOUR_PASSWORD> \
-e CORE_COUNT=3 \
-e VCPU_COUNT=3 \
-e VPN_PASSWORD=<YOUR_PASSWORD> \
-e VPN_ADDRESS=<YOUR_IP> \
-e VPN_USER=<YOUR_USER> \
-e VPN_SERVER_CERT=<YOUR_SERVERCERT> \
-e ANSIBLE_SSH_USER=<SYSTEM_USER> \
-e ANSIBLE_SSH_PASS=<SYSTEM_PASS> \
trial_env
```
