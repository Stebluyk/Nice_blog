FROM ubuntu:14.04

RUN apt-get update \
  && apt-get install -y python pip

COPY * /

RUN pip install -r requirements.txt \
     python manage.py makemigrations \
     python manage.py migrate \ 
     python manage.py runserver
     
CMD tail
