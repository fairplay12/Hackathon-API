from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hackathon',
        'USER': 'hackathon',
        'PASSWORD': 'hackathon123',
        'HOST': 'db',
        'PORT': '5432',
    }
}
