#!/usr/bin/env bash
python manage.py flush --no-input
python manage.py makemigrations --settings=webshop.settings.prod
python manage.py migrate --settings=webshop.settings.prod
python manage.py collectstatic --no-input
python manage.py runserver --settings=webshop.settings.prod 0.0.0.0:8000