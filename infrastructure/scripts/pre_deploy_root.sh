#!/bin/bash

# Install python 3.7 for Django project
yum install -y gcc openssl-devel bzip2-devel libffi-devel postgresql-devel
cd /usr/src
wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
tar xzf Python-3.7.3.tgz
cd Python-3.7.3
./configure --enable-optimizations
make altinstall
rm /usr/src/Python-3.7.3.tgz

# Install pip and virtualenv
cd ~
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
pip install virtualenv 

# Create user to host project 
useradd django 
echo "django" | passwd --stdin django

# TODO - move to system.sh provision script
# Install rsync
yum install -y rsync python-devel epel-release 
yum install -y nginx




