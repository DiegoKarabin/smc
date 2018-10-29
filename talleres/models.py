from django.db import models
from personas.models import Persona

# Create your models here.


class Grupo(models.Model):
    nombre = models.CharField(max_length=30, default='', primary_key=True)
    tematica = models.CharField(max_length=50, default='')
    participantes = models.ManyToManyField(Persona)
    fecha_inicio = models.DateField(default=None)
    fecha_final = models.DateField(default=None)

class Sesion(models.Model):
	PENDIENTE = 'Pendiente'
	REALIZADA = 'Realizada'
	CANCELADA = 'Cancelada'
	OPCIONES_ESTADO = (
		(PENDIENTE, 'Pendiente'),
		(REALIZADA, 'Realizada'),
		(CANCELADA, 'Cancelada'),
	)

	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
	fecha = models.DateField(default=None)
	estado = models.CharField(choices=OPCIONES_ESTADO, max_length=9)
	asistentes = models.ManyToManyField(Persona)
