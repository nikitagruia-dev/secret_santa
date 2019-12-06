#!/bin/bash

python manage.py migrate

if [ "$MANAGE_PY" = "True" ]; then
  echo "Start manage.py"

  python manage.py runserver ${GUNICORN_BIND} --noreload
else
  echo "Start GUNICORN"

  gunicorn --workers=${GUNICORN_WORKERS} --env DJANGO_SETTINGS_MODULE=config.${DJANGO_ENV} config.wsgi:application -b ${GUNICORN_BIND} --log-level info --timeout ${GUNICORN_TIMEOUT}
fi
