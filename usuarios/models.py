from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from administracion.models import *
# Create your models here.

class Pregunta(models.Model):
    pregunta = models.CharField(max_length=60)

class ManejadorUsuario(BaseUserManager):

    def create_user(self, ci, nombre, apellido, profesion, edit, password=None):
        if not ci:
            raise ValueError('El usuario debe tener una identificación')

        usuario = self.model(
            ci=ci,
            nombre=nombre,
            apellido=apellido,
            profesion=profesion,
            edit=edit
        )
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, ci, nombre, apellido, profesion, password):
        usuario = self.create_user(
            ci, nombre, apellido, profesion, password=password)
        usuario.is_admin = True
        usuario.is_password_setted = True
        usuario.save(using=self._db)
        ConfBDA = configuracionBDA.objects.filter(id = 1)
        if ConfBDA.exists() == False:
            ConfBDA = configuracionBDA(respaldo = 0, periodo = 'A')
            ConfBDA.save()
            print("Configuracion de la base de datos establecida correctamente")
        return usuario


class Usuario(AbstractBaseUser):
    ci = models.CharField('Identificación', max_length=9, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    profesion = models.CharField(max_length=30)
    email = models.EmailField()
    is_active = models.BooleanField('Activo', default=True)
    is_admin = models.BooleanField('Administrador', default=False)
    is_audit = models.BooleanField('Auditor', default=False)
    edit = models.BooleanField(default=False)
    is_editing = models.CharField(max_length=9, default=0)
    is_password_setted = models.BooleanField(default=False)
    is_security_question_setted = models.BooleanField(default=False)
    preguntas = models.ManyToManyField(Pregunta, through='PreguntaUsuario')

    objects = ManejadorUsuario()

    USERNAME_FIELD = 'ci'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'profesion']

    def __str__(self):
        return self.ci

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return self.nombre + ' ' + self.apellido

    def get_is_editing(self):
        return self.is_editing

class PreguntaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.CharField('Respuesta', max_length=80)

    def setRespuesta(self, respuesta):
        self.respuesta = make_password(respuesta)

    def es_respuesta_correcta(self, respuesta):
        return check_password(respuesta, self.respuesta)