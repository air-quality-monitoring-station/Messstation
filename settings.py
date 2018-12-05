import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# example) SQLite
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# example) MySQL
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'aqms',
         'USER': 'aqms',
         'PASSWORD': 'jnBDb33RmSPfycev',
         'HOST': '10.41.0.3',
         'PORT': '3306',
     }
 }


INSTALLED_APPS = (
    'data',
)

SECRET_KEY = 'REPLACE_ME'
