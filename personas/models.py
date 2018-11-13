from django.db import models

from datetime import date

# Create your models here.


class Persona(models.Model):
    IMPUTADO = 'Imputado'
    VICTIMA = 'Víctima'
    OPCIONES_CONDICION = (
        (IMPUTADO, 'Imputado'),
        (VICTIMA, 'Víctima')
    )

    SOLTERO = 'Soltero(a)'
    CASADO = 'Casado(a)'
    VIUDO = 'Viudo(a)'
    DIVORCIADO = 'Divorciado(a)'

    OPCIONES_ESTADO_CIVIL = (
        (SOLTERO, 'Soltero(a)'),
        (CASADO, 'Casado(a)'),
        (VIUDO, 'Viudo(a)'),
        (DIVORCIADO, 'Divorciado(a)')
    )

    SIN_ESTUDIOS = 'Sin estudios'
    PRIMARIA = 'Primaria'
    BACHILLER = 'Bachiller'
    TECNICO_MEDIO = 'Técnico Medio'
    UNIVERSITARIO = 'Universitario'

    OPCIONES_GRADO_INSTITUCION = (
        (SIN_ESTUDIOS, 'Sin estudios'),
        (PRIMARIA, 'Primaria'),
        (BACHILLER, 'Bachiller'),
        (TECNICO_MEDIO, 'Técnico Medio'),
        (UNIVERSITARIO, 'Universitario'),
    )

    MASCULINO = 'Masculino'
    FEMENINO = 'Femenino'

    OPCIONES_SEXO = (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino')
    )

    nombre = models.CharField(max_length=30, default='')
    apellido = models.CharField(max_length=30, default='')
    sexo = models.CharField(max_length=9, choices=OPCIONES_SEXO)
    lugar_de_nacimiento = models.CharField(max_length=50, default='', blank=True)
    fecha_de_nacimiento = models.DateField(default=None, blank=True, null=True)
    ci = models.PositiveIntegerField(
        'Cédula de Identidad', primary_key=True, default=0)
    estado_civil = models.CharField(
        max_length=13, choices=OPCIONES_ESTADO_CIVIL, blank=True)
    nacionalidad = models.CharField(max_length=30, default='', blank=True)
    grado_de_institucion = models.CharField(
        max_length=30, choices=OPCIONES_GRADO_INSTITUCION, blank=True)
    direccion = models.CharField(max_length=50, default='', blank=True)
    telefono = models.CharField(max_length=12, default='', blank=True)
    ocupacion = models.CharField(max_length=20, default='', blank=True)
    direccion_trabajo = models.CharField(max_length=50, default='', blank=True)
    condicion = models.CharField(
        'Condición', max_length=8, choices=OPCIONES_CONDICION, blank=True)
    edit = models.BooleanField(default=False)
    is_editing = models.CharField(max_length=9 ,default=0)

    @property
    def edad(self):
        if self.fecha_de_nacimiento:
            delta = date.today() - self.fecha_de_nacimiento
            return delta.days // 365
        else:
            return ''
