# Fro production environment
from .base import *

DEBUG = True

# Send errors to admin in ADMINS tuple with tuples
ADMINS = (
    ('Tomasz Z', 'tziss85@gmail.com')
)

ALLOWED_HOSTS = ['localhost','zizu','127.0.0.1']

# psycopg2 package is required to use postgresql database engine
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'educa',
        'USER': 'educa',
        'PASSWORD': 'educa'
    }
}

# Hardening part from check for deploy scan
#SECURE_HSTS_SECONDS = 60