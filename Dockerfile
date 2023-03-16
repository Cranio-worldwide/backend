# FROM python:3.9
# WORKDIR /app
# COPY . .
# RUN pip3 install -r /app/requirements.txt --no-cache-dir



FROM python:3.9.6-alpine
WORKDIR /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .