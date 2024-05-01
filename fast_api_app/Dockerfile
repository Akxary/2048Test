FROM python:3.11
LABEL authors="pollx"

WORKDIR /usr/src/fast_api_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

COPY . .

RUN poetry install

