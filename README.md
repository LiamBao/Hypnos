# Hypnos

> [django|celery|redis|rabitmq|docker|nginx|uwsgi]


## ***deployment*** :

###- ***Building docker images& Creating containers***

Since we are working with Docker, we need a proper Dockerfile to specify how our image will be built.
Customize the web image by  `/Hypnos/docker/Dockerfile_web`

***`cd`*** to your project

cmd: ***`chmod 777 $pwd`*** to avoid the privilege issue

cmd: ***`docker-compose build`***

logs:
~~~
(python3) ➜  Hypnos git:(master) ✗ docker-compose build
Building worker_default
Step 1/10 : FROM python:3
 ---> c1e459c00dc3
Step 2/10 : MAINTAINER "Liam Bao<liam_bao@163.com>"
 ---> Running in 1590b4cad68f
Removing intermediate container 1590b4cad68f
 ---> 0c79ce0e320a
Step 3/10 : ENV PYTHONUNBUFFERED 1
 ---> Running in e368301f7157
Removing intermediate container e368301f7157
 ---> c53442f49fd8
Step 4/10 : RUN mkdir -p /src/app
 ---> Running in a4f3274e08ba
Removing intermediate container a4f3274e08ba
 ---> 450faf4c5811
Step 5/10 : WORKDIR /src/app
Removing intermediate container 40e6de570041
 ---> 4edfda28b313
Step 6/10 : ADD requirements.txt /src/app/
 ---> 67e887cdc3c3
Step 7/10 : RUN pip install -r requirements.txt
 ---> Running in 9620d89010dc
Collecting Django (from -r requirements.txt (line 1))
....
.... 
Creating home directory `/home/liam' ...
Copying files from `/etc/skel' ...
Removing intermediate container 9b7ee7db90e6
 ---> 4a68dd8ef730
Step 10/10 : RUN chown -R liam:liam .
 ---> Running in 7b391a5f343d
Removing intermediate container 7b391a5f343d
 ---> 3229be780814
Successfully built 3229be780814
Successfully tagged hypnos_web:latest
~~~

verify the images
```
(python3) ➜  Hypnos git:(master) docker images
```
```
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
hypnos_web              latest              3229be780814        28 seconds ago      755MB
hypnos_worker_default   latest              af5e48e01ac7        32 seconds ago      755MB

```

you can exec into the imgaes to check pro files

cmd: ***` docker run -it --rm 3229be780814 /bin/bash`***

```
(python3) ➜  Hypnos git:(master) ✗ docker run -it --rm 3229be780814 /bin/bash
root@cbbe0cc9096c:/src/app# ls -lh
total 28K
-rw-r--r-- 1 liam liam 2.0K Jan 30 08:50 README.md
drwxr-xr-x 1 liam liam 4.0K Jan 30 07:12 docker
-rw-r--r-- 1 liam liam 1.3K Jan 30 08:17 docker-compose.yml
drwxr-xr-x 1 liam liam 4.0K Jan 30 08:16 hypnos
-rw-r--r-- 1 liam liam  128 Jan 30 07:27 requirements.txt
-rw-r--r-- 1 liam liam  363 Jan 30 07:31 run_celery.sh
-rw-r--r-- 1 liam liam  356 Jan 30 07:30 run_web.sh
```

docker up and check logs
```
(python3) ➜  Hypnos git:(master) ✗ docker-compose up
Starting hypnos_rabbit_1 ...
Starting hypnos_redis_1 ...
Starting hypnos_db_1 ... done
Creating hypnos_web_1    ... done
Attaching to hypnos_rabbit_1, hypnos_redis_1, hypnos_db_1, hypnos_web_1
redis_1   | 1:C 30 Jan 12:44:00.792 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1   | 1:C 30 Jan 12:44:00.792 # Redis version=4.0.7, bits=64, commit=00000000, modified=0, pid=1, just started
db_1      | 2018-01-30 12:44:00.931 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
...
...
web_1     | Operations to perform:
web_1     |   Apply all migrations: admin, auth, contenttypes, sessions
web_1     | Running migrations:
web_1     |   Applying contenttypes.0001_initial... OK
web_1     |   Applying auth.0001_initial... OK
web_1     |   Applying admin.0001_initial... OK
web_1     |   Applying admin.0002_logentry_remove_auto_add... OK
web_1     |   Applying contenttypes.0002_remove_content_type_name... OK
web_1     |   Applying auth.0002_alter_permission_name_max_length... OK
web_1     |   Applying auth.0003_alter_user_email_max_length... OK
web_1     |   Applying auth.0004_alter_user_username_opts... OK
web_1     |   Applying auth.0005_alter_user_last_login_null... OK
web_1     |   Applying auth.0006_require_contenttypes_0002... OK
web_1     |   Applying auth.0007_alter_validators_add_error_messages... OK
web_1     |   Applying auth.0008_alter_user_username_max_length... OK
web_1     |   Applying auth.0009_alter_user_last_name_max_length... OK
web_1     |   Applying sessions.0001_initial... OK
web_1     | Performing system checks...
web_1     |
web_1     | System check identified no issues (0 silenced).
web_1     | January 30, 2018 - 12:44:09
web_1     | Django version 2.0.1, using settings 'hypnos.settings'
web_1     | Starting development server at http://0.0.0.0:8801/
web_1     | Quit the server with CONTROL-C.
web_1     | INFO 2018-01-30 12:44:40,739 "GET / HTTP/1.1" 200 5222
```

Scaling out a container with docker-compose is extremely easy. Just use the docker-compose scale command with the container name and amount:

**```docker-compose scale worker_default=5```**
```
(python3) ➜  Hypnos git:(master) ✗ docker-compose ps
         Name                        Command                State                              Ports
-----------------------------------------------------------------------------------------------------------------------------
hypnos_db_1               docker-entrypoint.sh postgres    Up         0.0.0.0:5432->5432/tcp
hypnos_rabbit_1           docker-entrypoint.sh rabbi ...   Up         0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp,
                                                                      5671/tcp, 0.0.0.0:5672->5672/tcp
hypnos_redis_1            docker-entrypoint.sh redis ...   Up         0.0.0.0:6379->6379/tcp
hypnos_web_1              ./run_web.sh                     Up         0.0.0.0:8801->8801/tcp
hypnos_worker_default_1   ./run_celery.sh                  Up
hypnos_worker_default_2   ./run_celery.sh                  Up
hypnos_worker_default_3   ./run_celery.sh                  Up
```


###- ***setting up Django & Celery Tasks***

Creating users

```
(python3) ➜  Hypnos git:(master) ✗ docker-compose exec web bash
root@web:/src/app/hypnos# python manage.py shell
Python 3.6.4 (default, Dec 21 2017, 01:35:12)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('liam', 'liam_bao@example.com', 'Baokai2018')
>>> user.save()
```

Creating superusers

**`python manage.py createsuperuser --username=liam --email=liam@example.com`**

Monitoring logs

**```(python3) ➜  Hypnos git:(master) ✗ docker-compose logs -f web```**

The first script  
***`run_web.sh`***
will migrate the database and start the Django development server on port 8801. 

The second one  
***`run_celery.sh`***
will start a Celery worker listening on a queue default.



Visit 'http://localhost:8801/celery/jobs/'

output:
~~~
web_1             | INFO 2018-01-30 15:50:10,082 "GET /celery/jobs/ HTTP/1.1" 200 10359
worker_default_1  | INFO 2018-01-30 15:50:13,817 Received task: celery_test.tasks.fib[8199b13e-1501-4410-885c-19eab03017fd]
worker_default_1  | [2018-01-30 15:50:13,817: INFO/MainProcess] Received task: celery_test.tasks.fib[8199b13e-1501-4410-885c-19eab03017fd]
worker_default_1  | INFO 2018-01-30 15:50:13,828 Task celery_test.tasks.fib[8199b13e-1501-4410-885c-19eab03017fd] succeeded in 0.009696149005321786s: None
worker_default_1  | [2018-01-30 15:50:13,828: INFO/ForkPoolWorker-2] Task celery_test.tasks.fib[8199b13e-1501-4410-885c-19eab03017fd] succeeded in 0.009696149005321786s: None
web_1             | INFO 2018-01-30 15:50:13,843 "POST /celery/jobs/ HTTP/1.1" 201 10356
web_1             | INFO 2018-01-30 15:50:17,944 "OPTIONS /celery/jobs/ HTTP/1.1" 200 13411
web_1             | INFO 2018-01-30 15:50:25,743 "GET /celery/jobs/ HTTP/1.1" 200 10680
worker_default_1  | INFO 2018-01-30 15:50:39,201 Received task: celery_test.tasks.power[564c0af4-fb74-4cef-87de-2904159a1405]
worker_default_1  | [2018-01-30 15:50:39,201: INFO/MainProcess] Received task: celery_test.tasks.power[564c0af4-fb74-4cef-87de-2904159a1405]
worker_default_1  | INFO 2018-01-30 15:50:39,215 Task celery_test.tasks.power[564c0af4-fb74-4cef-87de-2904159a1405] succeeded in 0.012064064998412505s: None
worker_default_1  | [2018-01-30 15:50:39,215: INFO/ForkPoolWorker-2] Task celery_test.tasks.power[564c0af4-fb74-4cef-87de-2904159a1405] succeeded in 0.012064064998412505s: None
web_1             | INFO 2018-01-30 15:50:39,239 "POST /celery/jobs/ HTTP/1.1" 201 10352
worker_default_1  | INFO 2018-01-30 15:50:41,772 Received task: celery_test.tasks.power[2e876b75-c732-4975-94f6-8c1331cad143]
worker_default_1  | [2018-01-30 15:50:41,772: INFO/MainProcess] Received task: celery_test.tasks.power[2e876b75-c732-4975-94f6-8c1331cad143]
worker_default_1  | INFO 2018-01-30 15:50:41,783 Task celery_test.tasks.power[2e876b75-c732-4975-94f6-8c1331cad143] succeeded in 0.009442675996979233s: None
worker_default_1  | [2018-01-30 15:50:41,783: INFO/ForkPoolWorker-2] Task celery_test.tasks.power[2e876b75-c732-4975-94f6-8c1331cad143] succeeded in 0.009442675996979233s: None
web_1             | INFO 2018-01-30 15:50:41,799 "POST /celery/jobs/ HTTP/1.1" 201 10352
rabbit_1          | missed heartbeats from client, timeout: 30s
~~~



###- ***Setting up Django and web server with uWSGI and nginx***

> `for doc: https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html`

#### ***nginx*** (pronounced engine-x) 

is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.
nginx and uWSGI are good choices for Django deployment, but they are not the only ones, or the ‘official’ ones. There are excellent alternatives to both, and you are encouraged to investigate them.

#### ***uWSGI***

A web server faces the outside world. It can serve files (HTML, images, CSS, etc) directly from the file system. However, it can’t talk directly to Django applications; it needs something that will run the application, feed it requests from web clients (such as browsers) and return responses.

A Web Server Gateway Interface does this job. WSGI is a Python standard.

uWSGI is a WSGI implementation. In this tutorial we will set up uWSGI so that it creates a Unix socket, and serves responses to the web server via the uwsgi protocol. At the end, our complete stack of components will look like this:

**```the web client <-> the web server <-> the socket <-> uwsgi <-> Django```**

