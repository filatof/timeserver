#FROM python:3.12-alpine
FROM python:3.14.0rc1-slim-bullseye
# Отключает буферизацию вывода Python (в stdout/stderr), чтобы логирование сразу попадало в Docker-логи
ENV PYTHONUNBUFFERED=1

# Копирует текущую директорию (с host) в контейнер
COPY . /app

# Назначает рабочую директорию внутри контейнера
WORKDIR /app

# Запускает сервер
CMD ["python3", "server.py"]