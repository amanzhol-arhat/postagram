FROM python:3.13-alpine


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=CoreRoot.settings.prod

RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev


COPY req.txt /app/req.txt


RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r req.txt


COPY . .
