#! /bin/bash

set -e

echo "Waiting for postgres..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.5
done
echo "PostgreSQL started"

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --noinput

gunicorn -w 5 application.wsgi:application -b 0.0.0.0:8000 --reload --timeout 120
