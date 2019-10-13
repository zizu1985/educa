#!/bin/bash

# Install Postgresql 11
yum install -y https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-7-x86_64/pgdg-centos11-11-2.noarch.rpm            
yum install -y postgresql11-server postgresql11-contrib

/usr/pgsql-11/bin/postgresql-11-setup initdb
systemctl start postgresql-11
systemctl enable postgresql-11

# Create Database and user for educa application
sudo su - postgres -c "createdb educa"
sudo su - postgres -c "createuser -l educa"
sudo su - postgres -c "psql -c \"ALTER USER educa WITH PASSWORD 'educa'\""

# Modify pg_hba.conf file to allow local connections using password
HBA_PATH=`find / -name 'pg_hba.conf' 2>/dev/null`
if [ ! -z "$HBA_PATH" ]
then 
    LN=`cat $HBA_PATH | grep -nE "local.*all.*all" | cut -d: -f1`
    if [ ! -z "LN" ]
    then
        echo "sed -i "${LN}s/peer/md5/" $HBA_PATH"
        sed -i "${LN}s/peer/md5/" $HBA_PATH
    fi
    for LN in `cat $HBA_PATH | grep -nE "host.*all.*all" | cut -d: -f1`
    do
        if [ ! -z "LN" ]
        then
            echo "sed -i "${LN}s/ident/md5/" $HBA_PATH"
            sed -i "${LN}s/ident/md5/" $HBA_PATH
        fi
    done
fi

# Restart Postgresql to make change happend
systemctl stop postgresql-11
systemctl start postgresql-11

