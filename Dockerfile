FROM ubuntu:22.04

MAINTAINER mcieciora

RUN apt-get update && apt-get install -y python3-pip python3-dev

COPY ./src /app

COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3.10" ]

CMD [ "api.py" ]