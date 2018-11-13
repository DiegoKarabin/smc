from django.db import models
from datetime import date
# Create your models here.


class configuracionBDA(models.Model):
	respaldo = models.IntegerField()
	periodo = models.CharField(max_length=1)
	ultimo_respaldo = models.DateTimeField(default=None, blank=True, null=True)
	ultima_importacion = models.DateTimeField(default=None, blank=True, null=True)
	uitima_exportacion = models.DateTimeField(default=None, blank=True, null=True)

class Bitacora(models.Model):
	fecha = models.DateField(default = date.today)
	descripcion = models.CharField(max_length = 15)

	

