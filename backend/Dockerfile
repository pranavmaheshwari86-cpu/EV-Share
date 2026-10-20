# Production Dockerfile for EV Share
# Python 3.12, Django 6.1, Gunicorn, WhiteNoise, MongoEngine
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend source
COPY backend/ ./backend/
COPY frontend/ ./frontend/

WORKDIR /app/backend

# Collect static assets into staticfiles
RUN python manage.py collectstatic --noinput || true

# Security: Non-privileged user
RUN useradd -m evshare && chown -R evshare:evshare /app
USER evshare

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-"]
