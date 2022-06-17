#!/bin/bash
source .env

debug=$(cat config.yaml | shyaml get-value DEBUG)

echo "Starting server, debug mode: $debug"

if [ $debug = "True" ]; then
  ./manage.py runserver 0.0.0.0:$DJANGO_PORT
else
  gunicorn --bind :$DJANGO_PORT --workers 8 src.wsgi:application
fi
