# Используем Alpine, как ты и хотел
FROM python:3.13-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Настройки Python, чтобы логи выводились сразу и не плодились .pyc файлы
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Устанавливаем системные зависимости для Alpine
# Внимание: исправил опечатки (musl-dev) и добавил зависимости для Pillow (jpeg, zlib)
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    libffi-dev

# Копируем файл зависимостей
COPY req.txt /app/req.txt

# Обновляем pip и устанавливаем пакеты
RUN pip install --upgrade pip
# Исправил опечатку в названии файла (-req.txt -> req.txt)
RUN pip install --no-cache-dir -r req.txt

# Копируем весь проект в образ
COPY . .

