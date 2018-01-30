#!/bin/sh

# wait for PSQL server to start
sleep 5

cd /src/app/hypnos
# prepare init migration
su -m liam -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
su -m liam -c "python manage.py migrate"  
# start development server on public ip interface, on port 8000
su -m liam -c "python manage.py runserver 0.0.0.0:8801"