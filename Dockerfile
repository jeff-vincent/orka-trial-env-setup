FROM python:3.10.0-alpine3.14
RUN apk update && \
    apk add --update \
	ansible \
	bash \
	curl \
    openssh \
    sshpass && \
    apk add --upgrade openconnect && \
    python3 -m pip install requests
COPY . .
ENTRYPOINT ["./run.sh"]
