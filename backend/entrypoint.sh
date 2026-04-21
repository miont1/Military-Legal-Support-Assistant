#!/bin/bash
set -e

# Strip Windows CRLF from environment variables
for var in $(env | grep -oP '^[^=]+'); do
    val="$(printenv "$var" 2>/dev/null || true)"
    clean_val="$(echo "$val" | tr -d '\r')"
    if [ "$val" != "$clean_val" ]; then
        export "$var"="$clean_val"
    fi
done

echo "Waiting for PostgreSQL at ${DB_HOST:-db}:${DB_PORT:-5432}..."
while ! python -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(('${DB_HOST:-db}', ${DB_PORT:-5432}))
    s.close()
    exit(0)
except Exception:
    exit(1)
" 2>/dev/null; do
    echo "PostgreSQL is unavailable - sleeping..."
    sleep 2
done
echo "PostgreSQL is up!"

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
exec gunicorn diplom.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
