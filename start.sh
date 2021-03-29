#!/bin/bash
#useradd -M celery
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
sed -i '65 s/value.id = value.text;/value.id = value.id;/' /app/.heroku/python/lib/python3.6/site-packages/dal_select2/static/autocomplete_light/select2.js
python manage.py collectstatic --noinput --settings=apis.settings.server
python manage.py migrate --settings=apis.settings.server
gunicorn apis.wsgi
