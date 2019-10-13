#!/bin/bash

# Create work directory for project
sudo su - django -c "mkdir /home/django/educa"
sudo su - django -c "cd /home/django/educa ; virtualenv venv"
#sudo su - django -c "cp -r `ls -A /educa/* | grep -v "venv"` /home/django/educa/"
sudo su - django -c "rsync -arv --exclude=venv /educa /home/django/educa"
sudo su - django -c "cp /educa/requirments.txt /home/django/educa/requirments.txt"
sudo su - django -c "chown django:django /home/django/educa/requirments.txt"
sudo su - django -c "chown -R django:django /home/django/educa"
sudo su - django -c "source /home/django/educa/venv/bin/activate ; pip install -r /home/django/educa/requirments.txt"

# Install uWSGI
sudo su - django -c "source /home/django/educa/venv/bin/activate ; pip install uwsgi==2.0.11.1"

# Migrate models to database
sudo su - django -c "source /home/django/educa/venv/bin/activate ; cd /home/django/educa/educa ; python manage.py migrate --settings=educa.settings.pro"