#!/bin/bash

echo "Running collectstatic"
python ${APP_DIR}/backend/manage.py collectstatic --noinput
echo "Running migrations"
python ${APP_DIR}/backend/manage.py migrate --noinput

/usr/bin/supervisord
