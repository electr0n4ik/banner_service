FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY ./requirements.txt .

RUN apt-get update
RUN apt-get install -y build-essential libssl-dev libffi-dev libpq-dev gcc wget

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
