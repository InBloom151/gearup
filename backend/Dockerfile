# ---------- build dependencies ----------
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# system deps (asyncpg compiling)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# ---------- runtime (prod) ----------
FROM python:3.11-slim-bookworm AS prod

ENV PYTHONBUFFERED=1 \
    PATH="/install/bin:$PATH"

WORKDIR /app

COPY --from=builder /install /usr/local
COPY backend /app

RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app
USER appuser

ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]

# ---------- runtime (dev) ----------
FROM prod AS dev
ENV APP_ENV=development
ENTRYPOINT [ "/app/scripts/entrypoint-dev.sh" ]
