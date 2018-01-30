#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd /src/app/hypnos
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m liam -c "celery worker -A hypnos.celeryconf -Q default -n default@%h"  

#for test
# su -m liam -c "celery worker -A hypnos -Q default -n worker_default@%h -l INFO -f logs/worker_default@%h.log"