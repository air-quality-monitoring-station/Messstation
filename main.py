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
voc = os.system('./Airsensor/usb-sensors-linux/trunk/airsensor/airsensor -o -v')
feinstaub2 = os.system('./Feinstaub2')
feinstaub10 = os.system('./Feinstaub10')
sense = SenseHat()
temperature = sense.get_temperature()
pressure = sense.get_pressure()
humidity = sense.get_humidity()

# uuid, remove -
uuidnum = uuid.uuid4()
uuidstr = str(uuidnum)
for letter in '-':
    sos = uuidstr.replace(letter, '')
    finalid = sos
# timestamp
# date
tmstp = datetime.date.today()
# datetime
dattime = datetime.datetime.now()


sense.show_message("#", scroll_speed=1)
