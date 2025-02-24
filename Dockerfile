FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/src

COPY .env .env

COPY alembic.ini .

COPY migrations migrations

EXPOSE 8000

ENV HOST=0.0.0.0

CMD ["uvicorn","src:app","--port","8000","--host","0.0.0.0"]
