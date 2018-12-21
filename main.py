# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from data.models import *


# Add user
#user = User(name="masnun", email="masnun@gmail.com")
#user.save()


# Application logic
import time
import uuid
import datetime
import traceback
from sense_hat import SenseHat
command = "cmd"

# Variables
voc = os.system('./airsensor -o -v')
feinstaubpm25 = os.system('./Feinstaub2.py')
feinstaubpm100 = os.system('./Feinstaub10.py')
sense = SenseHat()
temperatur = sense.get_temperature()
luftdruck = sense.get_pressure()
luftfeuchtigkeit = sense.get_humidity()

# uuid, remove -
uuidnum = uuid.uuid4()
uuidstr = str(uuidnum)
for letter in '-':
    uid = uuidstr.replace(letter, '')
    finalid = uid
# timestamp
# date
datum = datetime.date.today()
# datetime
datumzeit = datetime.datetime.now()

# Objects
messdaten = Messdaten(UID=uid, Temperatur=temperatur, Luftdruck=luftdruck, Luftfeuchtigkeit=luftfeuchtigkeit, VOC=voc, FEINSTAUBPM25=feinstaubpm25, FEINSTAUBPM100=feinstaubpm100, Datum=datum, DatumZeit=datumzeit)
messdaten.save() 


sense.show_message("#", scroll_speed=1)
