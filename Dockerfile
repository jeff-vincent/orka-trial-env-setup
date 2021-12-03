FROM python:3.10.0-alpine3.14
RUN apk update
RUN apk add ansible
RUN apk add bash
RUN apk add --upgrade openconnect
COPY . .
ENTRYPOINT ["./run.sh"]
