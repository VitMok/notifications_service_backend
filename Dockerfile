FROM python:3.10-slim

ENV VAR1=10

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

RUN pip install pipenv

WORKDIR /usr/src/notification_service_backend

COPY . .

RUN pipenv install --dev --system --deploy
# RUN pipenv install --system --deploy
# RUN pipenv install --deploy --ignore-pipfile
