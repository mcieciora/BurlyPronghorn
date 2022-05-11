FROM ubuntu:22.04

MAINTAINER mcieciora

RUN apt-get update && apt-get install -y python3-pip python3-dev

COPY src/ /app/src/

COPY automated_tests/ /app/automated_tests/

COPY requirements.txt /app/automated_tests/

WORKDIR /app

RUN pip install -r automated_tests/requirements.txt

RUN pip install -r automated_tests/test-requirements.txt

ENTRYPOINT [ "python3.10" ]