FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY ./requirements.txt .
COPY ./core .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
