# Django specific settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Django imports
from django.core.management.base import BaseCommand

# Application specific imports

# standard libs
import uuid
import datetime
import threading
import queue

# other libs
from sense_hat import SenseHat

# models
from aqms.models import *

# queues for communication between threads
q_gen_messdaten = queue.Queue()
q_to_db = queue.Queue()

class Command(BaseCommand):
    
    # Application logic,
    def handle(self, *args, **kwargs):
        print("get data")
        try:
            pill2kill = threading.Event()  # -> cyanide pills

            gen_messdaten_thread = threading.Thread(target=SENSORIO.gen_messdaten_t, args=(pill2kill,))
            gen_messdaten_thread.daemon = True  # -> dies after main thread is closed
            gen_messdaten_thread.start()

            to_db_thread = threading.Thread(target=DBIO.to_db_t, args=(pill2kill,))
            to_db_thread.daemon = True  # -> dies after main thread is closed
            to_db_thread.start()

            #SenseHat.show_message("#", scroll_speed=1)
        
        finally:
            pill2kill.set()
            gen_messdaten_thread.join()
            to_db_thread.join()
            #return ('done', arg_counter)

# SENSORIO class -> handles all input/output from/to the sensors
class SENSORIO:
    # meths
    @staticmethod
    def gen_messdaten_t(pill2kill):  # <- code of gen_messdaten_t thread

        #fe_log = None

        try:
            while not pill2kill.is_set():
                try:
                    q_gen_messdaten.put(MESSDATEN())
                    q_gen_messdaten.task_done()

                except Exception as e:
                    #fe_log = FILEIO.write_to_log('fe_log.txt', f'S_LINK_Error: {e}\n{traceback.format_exc()}')
                    continue

        finally:
            #if fe_log:
            #    CLIIO.print_to_shell('file create_slink_t error -> {root_dir}fe_log.txt')
            print('create_slink_t closed')

# DBIO class -> handles all input/output from/to database
class DBIO:
    # meths
    @staticmethod
    def to_db_t(pill2kill):  # <- code of to_db_t thread
        
        #dbe_log = None

        try:
            while not pill2kill.is_set() or q_to_db.full():

                messdaten = q_to_db.get(block=True)  # -> wait for input
                
                if isinstance(messdaten, MESSDATEN):
                    values_for_db = messdaten.for_db()

                    # push to db
                    messdaten_db = Messdaten(UID=values_for_db['uuid'], Temperatur=values_for_db['temperatur'], Luftdruck=values_for_db['luftdruck'], Luftfeuchtigkeit=values_for_db['luftfeuchtigkeit'], VOC=values_for_db['voc'], FEINSTAUBPM25=values_for_db['feinstaubpm25'], FEINSTAUBPM100=values_for_db['feinstaubpm100'], Datum=values_for_db['datum'], DatumZeit=values_for_db['datumzeit'])
                    messdaten_db.save() 

                q_to_db.task_done()
        finally:
            #if fe_log:
            #    CLIIO.print_to_shell('file create_slink_t error -> {root_dir}fe_log.txt')
            print('to_db_t closed')

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
        self._voc = os.popen('aqms/external/c/airsensor -o -v').read().rstrip('\n')
        self._feinstaubpm25 = os.popen('aqms/external/bash/Feinstaub25.sh').read().rstrip('\n')
        self._feinstaubpm100 = os.popen('aqms/external/bash/Feinstaub100.sh').read().rstrip('\n')
        self._datum = datetime.date.today()
        self._datumzeit = datetime.datetime.now()

    def __repr__(self):
            return str(self.__class__.__name__) + '; ' + str(self._datumzeit)

    def __str__(self):
            return str(self._uuid) + '; ' + \
                   str(self._temperatur) + '; ' + \
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
