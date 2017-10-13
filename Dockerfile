FROM python:3.6.3

ENV DATABASE_URL="postgres://postgres:postgres@db:5432/postgres" PYTHONUNBUFFERED=1
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
