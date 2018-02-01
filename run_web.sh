#!/bin/sh

# # wait for PSQL server to start
sleep 10
PROJECT_PATH=/src/app

cd /src/app/hypnos
# prepare init migration
su -m liam -c "python manage.py makemigrations"
# migrate db, so we have the latest db schema
su -m liam -c "python manage.py migrate"  
#collection all the static files to /staic
su -m liam -c "python manage.py collectstatic  --noinput"


#server test
#>>>>>>>>>>>>>>>>>>>>>>
#Scaling out a container with docker-compose is extremely easy. Just use the docker-compose scale command with the container name and amount when you dont need uwsgi:
# su -m liam -c "docker-compose scale worker_default=5" 
# start development server on public ip interface, on port 8801
###   FOR DEV
# su -m liam -c "python manage.py runserver 0.0.0.0:8801"
#<<<<<<<<<<<<<<<<<<<<<<



su -m liam -c " rm -rf ${PROJECT_PATH}/uwsgi.ini "
su -m liam -c "rm -rf ${PROJECT_PATH}/hpnos/static"
su -m liam -c "echo '' > ${PROJECT_PATH}/hypnos/logs/debug.log"
# su -m liam -c "rm -rf ${PROJECT_PATH}/nginx/logs && mkdir ${PROJECT_PATH}/nginx/logs"

# generate config file for uwsgi
#https type
cat > /src/app/uwsgi.sample <<EOF
;uWSGI instance configuration
[uwsgi]
;for https
chdir             = $PROJECT_PATH/hypnos
socket            = 127.0.0.1:8801
module            = hypnos.wsgi:application 
master            = true
http-auto-chunked = true
http-raw-body     = true
enable-threads    = true
die-on-term       = true
listen            = 1000
post-buffering    = 1
daemonize         = logs/console.log
# maximum number of worker processes
processes         = 2
threads           = 4
# clear environment on exit
vacuum          = true
EOF


# socket type to speed the performance
cat > ${PROJECT_PATH}/uwsgi.ini <<EOF
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = $PROJECT_PATH/hypnos
# Django's wsgi file
module          = hypnos.wsgi:application
# the virtualenv (full path)
# home            = /path/to/virtualenv
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 2
threads=2
# the socket (use the full path to be safe
socket          = $PROJECT_PATH/hypnos/app.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 664
# clear environment on exit
vacuum          = true

EOF

sleep 10
## start uwsgi
su -m liam -c "uwsgi --ini ${PROJECT_PATH}/uwsgi.ini"