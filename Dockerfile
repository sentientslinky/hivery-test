FROM alpine:3.7
RUN apk add --no-cache mysql-client
RUN apk add mysql
RUN apk add python
RUN apk add py-pip

COPY * /hivery/

CMD tail /dev/null