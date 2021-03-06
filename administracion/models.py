from django.db import models
from datetime import date
# Create your models here.


class configuracionBDA(models.Model):
	respaldo = models.IntegerField()
	periodo = models.CharField(max_length=1)
	ultimo_respaldo = models.DateField(default=None, blank=True, null=True)
	ultima_importacion = models.DateField(default=None, blank=True, null=True)
	uitima_exportacion = models.DateField(default=None, blank=True, null=True)

class Bitacora(models.Model):
	fecha = models.DateField(default = date.today)
	descripcion = models.CharField(max_length = 15)

class BitacoraTransaccion(models.Model):
	fecha = models.DateField(default = date.today)
	accion = models.CharField(max_length=80)
	tabla = models.CharField(max_length=80, blank=True)
	campo = models.CharField(max_length=80, blank=True)
	registro = models.CharField(max_length=80, blank=True)
	valor_anterior = models.CharField(max_length=80, blank=True)
	valor_actual = models.CharField(max_length = 80, blank=True)