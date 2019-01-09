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
#from sense_hat import SenseHat

# models
from aqms.models import *

class Command(BaseCommand):
    
    # Application logic
    def handle(self, *args, **kwargs):
        print("get data")
        # Variables
        #voc = os.system('./airsensor -o -v')
        #feinstaubpm25 = os.system('./Feinstaub2.py')
        #feinstaubpm100 = os.system('./Feinstaub10.py')
        #sense = SenseHat()
        #temperatur = sense.get_temperature()
        #luftdruck = sense.get_pressure()
        #luftfeuchtigkeit = sense.get_humidity()
        self.messdaten = MESSDATEN()
        # Variables
        self.temperatur = 22
        self.luftdruck = 949
        self.luftfeuchtigkeit = 53
        self.voc = 2.5864
        self.feinstaubpm25= 4.279
        self.feinstaubpm100 = 5.627

        values_for_db = self.messdaten.for_db()

        print(self.messdaten)
        print(self.messdaten.get_uuid())
        # uuid, remove -
        self.uuid = str(uuid.uuid4())
        print("fak2")
        # timestamp
        # date
        self.datum = datetime.date.today()
        # datetime
        self.datumzeit = datetime.datetime.now()

        
        # Objects
        messdaten = Messdaten(UID=values_for_db['uuid'], Temperatur=values_for_db['temperatur'], Luftdruck=values_for_db['luftdruck'], Luftfeuchtigkeit=values_for_db['luftfeuchtigkeit'], VOC=values_for_db['voc'], FEINSTAUBPM25=values_for_db['feinstaubpm25'], FEINSTAUBPM100=values_for_db['feinstaubpm100'], Datum=values_for_db['datum'], DatumZeit=values_for_db['datumzeit'])
        messdaten.save() 

        #sense.show_message("#", scroll_speed=1)

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
        self._uuid = str(uuid.uuid4())
        self._temperatur = 22
        self._luftdruck = 949
        self._luftfeuchtigkeit = 53
        self._voc = 2.5864
        self._feinstaubpm25= 4.279
        self._feinstaubpm100 = 5.627
        self._datum = datetime.date.today()
        self._datumzeit = datetime.datetime.now()

    def __repr__(self):
            return f'{self.__class__.__name__}({self._datumzeit})'

    def __str__(self):
            return f'{self._uuid}, {self._luftdruck}, {self._luftfeuchtigkeit}, {self._voc}, {self._feinstaubpm25}, {self._feinstaubpm100}, {self._datum}, {self._datumzeit}'

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
