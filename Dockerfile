# Dockerfile for azuresshconfig (Azure SSH Config)

FROM alpine:3.5
MAINTAINER Yoichi Kawasaki <https://github.com/yokawasa/azure-ssh-config>

RUN apk add --no-cache gcc python python-dev musl-dev openssl-dev libffi-dev && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    pip install azuresshconfig && \
    apk del --purge python-dev musl-dev openssl-dev libffi-dev && \
    rm -r /root/.cache

ENTRYPOINT ["azuresshconfig"]
