FROM python:3.10-slim

RUN mkdir -p /src
COPY src/ /src/

RUN pip install -r /src/requirements.txt

WORKDIR /src
