#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate_schemas
python manage.py migrate

gunicorn -b 0.0.0.0:8000 -w 4 --threads 2 app.wsgi
