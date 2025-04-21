#!/usr/bin/env bash
set -e

exec gunicorn app.main:app \
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:${BACKEND_PORT:-8000} \
     --workers ${WORKERS:-4}
