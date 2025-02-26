FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

COPY .env.docker .env.docker

COPY alembic.ini .

COPY migrations migrations
