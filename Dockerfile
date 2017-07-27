FROM ubuntu:14.04

RUN apt-get update \
  && apt-get install -y python3 pip postgresql postgresql-contrib

COPY * /

RUN pip install -r requirements.txt \
     python manage.py makemigrations \
     python manage.py migrate \ 
     python manage.py runserver
     
CMD tail
