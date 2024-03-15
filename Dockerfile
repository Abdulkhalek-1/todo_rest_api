FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update
RUN apt-get install -y libpq-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install  --no-cache-dir -r requirements.txt

COPY . .
