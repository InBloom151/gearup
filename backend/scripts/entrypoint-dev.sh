#!/usr/bin/env bash
set -e

./scripts/migrate.sh

exec uvicorn app.main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000} --reload
