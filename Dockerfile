FROM python:3.10.0-alpine3.14
RUN apk update
RUN apk add --update \
	ansible \
	bash \
	curl \
    openssh \
    sshpass
RUN apk add --upgrade openconnect
RUN python3 -m pip install requests
COPY . .
RUN python3 set_env.py
ENTRYPOINT ["./run.sh"]
