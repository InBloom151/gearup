#!/bin/sh
set -e

# ./wait-for-it.sh db:5432 -t 30

echo "Применение миграций Alembic..."
alembic upgrade head

echo "Запуск приложения FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload