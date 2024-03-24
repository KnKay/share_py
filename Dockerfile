FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

COPY setup.* /root

RUN cd /root && \
    pip install . && \
    pip install .[tests]
