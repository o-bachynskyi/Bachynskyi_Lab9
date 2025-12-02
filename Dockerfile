FROM python:3.11

RUN pip install --no-cache-dir psycopg2-binary sqlalchemy pandas tabulate

WORKDIR /app
