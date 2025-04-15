#!/bin/sh
set -e

# Ожидание готовности базы данных
until pg_isready -h db -p 5432 -U admin -d gearup; do
  echo "Ожидание базы данных..."
  sleep 1
done
echo "База данных доступна!"

echo "Применение миграций Alembic..."
alembic upgrade head

echo "Запуск приложения FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload