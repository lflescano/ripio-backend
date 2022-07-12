#!/bin/sh
python manage.py migrate
gunicorn backend.wsgi:application \
    --name rafam \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --log-level=info \
    --timeout 120 \
    --worker-class gevent \
"$@"

