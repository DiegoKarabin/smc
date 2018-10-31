from django.db import models
from datetime import date
# Create your models here.


class configuracionBDA(models.Model):
	respaldo = models.IntegerField()
	periodo = models.CharField(max_length=1)

class Bitacora(models.Model):
	ultima_respaldo = models.DateField(date.today())
	ultima_importacion = models.DateField(date.today())
	ultima_restauracion = models.DateField(date.today())

