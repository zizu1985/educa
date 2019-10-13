This is simple Django project (still under development) with deploy action into Centos 7 (using Vagrant).
The main goal of this work is to deploy django code into linux box with Nginx as front sever and uWSGI as backend for Django application.

Instruction:

1. After download please switch to infrastructure directory and start build and deploy application into 
  VirtualBox Machine using Vagrant:

  vagrant up

2. After successfull creation plase logon to machine using vagrant ssh and create super account:

  vagrant ssh
  sudo su - 
  su - django
  cd educa
  . venv/bin/activate
  python manage.py createsuperuser --settings=educa.settings.pro

3. Logon to webpage http://localhost:81/admin/ and craete new subject

4. Logon to webpage http://localhost:81/course/mine , logon as created superuser and create new course 
   under created subject.
