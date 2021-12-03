FROM python:3.10.0-alpine3.14
RUN apk update
RUN apk add ansible
RUN apk add bash
RUN apk add curl
RUN apk add --upgrade openconnect
RUN python3 -m pip install requests
COPY . .
ENTRYPOINT ["./run.sh"]
