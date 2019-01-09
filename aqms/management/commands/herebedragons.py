# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Django imports
from django.core.management.base import BaseCommand

# Application specific imports

# standard libs
import uuid
import datetime
import traceback

# other libs
from sense_hat import SenseHat

# models
from aqms.models import *

class Command(BaseCommand):
    
    # Application logic,
    def handle(self, *args, **kwargs):
        print("get data")

        self.messdaten = MESSDATEN()

        values_for_db = self.messdaten.for_db()

        print(self.messdaten)
        print(self.messdaten.get_uuid())

        # push to db
        messdaten = Messdaten(UID=values_for_db['uuid'], Temperatur=values_for_db['temperatur'], Luftdruck=values_for_db['luftdruck'], Luftfeuchtigkeit=values_for_db['luftfeuchtigkeit'], VOC=values_for_db['voc'], FEINSTAUBPM25=values_for_db['feinstaubpm25'], FEINSTAUBPM100=values_for_db['feinstaubpm100'], Datum=values_for_db['datum'], DatumZeit=values_for_db['datumzeit'])
        messdaten.save() 

        #SenseHat.show_message("#", scroll_speed=1)

# super EVIL object -> data of folders
class MESSDATEN:
    # fields
    _uuid = ''
    _temperatur = 22
    _luftdruck = 949
    _luftfeuchtigkeit = 53
    _voc = 2.5864
    _feinstaubpm25= 4.279
    _feinstaubpm100 = 5.627
    _datum = ''
    _datumzeit = ''

    # ctor
    def __init__(self):
        # initialize sensor
        sense = SenseHat()
        
        # define data
        self._uuid = str(uuid.uuid4())
        self._temperatur = sense.get_temperature()
        self._luftdruck = sense.get_pressure()
        self._luftfeuchtigkeit = sense.get_humidity()
        self._voc = os.system('./airsensor -o -v')
        self._feinstaubpm25 = 0 #os.system('../../bash/Feinstaub25.py')
        self._feinstaubpm100 = 0 #os.system('../../Feinstaub100.py')
        self._datum = datetime.date.today()
        self._datumzeit = datetime.datetime.now()

    def __repr__(self):
            return str(self.__class__.__name__) + '; ' + str(self._datumzeit)

    def __str__(self):
            return str(self._uuid) + '; ' + \
                   str(self._luftdruck) + '; ' + \
                   str(self._luftfeuchtigkeit) + '; ' + \
                   str(self._voc) + '; ' + \
                   str(self._feinstaubpm25) + '; ' + \
                   str(self._feinstaubpm100) + '; ' + \
                   str(self._datum) + '; ' + \
                   str(self._datumzeit)

    # props
    def get_uuid(self):
        return self._uuid

    def for_db(self):
        return {
            'uuid': self._uuid,
            'temperatur': self._temperatur,
            'luftdruck': self._luftdruck,
            'luftfeuchtigkeit': self._luftfeuchtigkeit,
            'voc': self._voc,
            'feinstaubpm25': self._feinstaubpm25,
            'feinstaubpm100': self._feinstaubpm100,
            'datum': self._datum,
            'datumzeit': self._datumzeit
        }
