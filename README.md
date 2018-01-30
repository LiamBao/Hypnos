# Hypnos
> [django|celery|redis|rabitmq|docker|nginx]


###***deployment*** :
- ***Build docker images&containers**

`cd` to your project

`chmod 777 $pwd` to avoid the privilege issue

`docker-compose build`

logs:
```
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
```

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
```

- 2. 