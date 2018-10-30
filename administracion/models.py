from django.db import models
from datetime import date
# Create your models here.


class configuracionBDA(models.Model):
	respaldo = models.BooleanField()
	periodo = models.CharField(max_length=1)
	ultima_respaldo = models.DateField(default = date.today())
	ultima_importacion = models.DateField(default = date.today())
	ultima_restauracion = models.DateField(default = date.today())

