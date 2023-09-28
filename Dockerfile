FROM python:3.9-slim

ARG BASIC_AUTH_USERNAME
ARG BASIC_AUTH_PASSWORD

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME
ENV BASIC_AUTH_PASSWORD=$BASIC_AUTH_PASSWORD

WORKDIR /app_docker

COPY requirements2.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./models /app_docker/models
COPY ./src /app_docker/src

ENTRYPOINT [ "python3" ]

CMD [ "src/app/main.py" ]