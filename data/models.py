import sys
import uuid

try:
    from django.db import models
except  Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Sample User model
class Messdaten(models.Model):
    UID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Temperatur= models.FloatField()
    Luftdruck= models.FloatField()
    Luftfeuchtigkeit = models.FloatField()
    VOC = models.FloatField()
    FEINSTAUBPM25 = models.FloatField()
    FEINSTAUBPM100 = models.FloatField()
    Datum = models.DateField()
    DatumZeit = models.DateTimeField()
