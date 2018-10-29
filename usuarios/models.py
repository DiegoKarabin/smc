from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class ManejadorUsuario(BaseUserManager):

    def create_user(self, ci, nombre, apellido, profesion, password=None):
        if not ci:
            raise ValueError('El usuario debe tener una identificación')

        usuario = self.model(
            ci=ci,
            nombre=nombre,
            apellido=apellido,
            profesion=profesion
        )
        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, ci, nombre, apellido, profesion, password):
        usuario = self.create_user(
            ci, nombre, apellido, profesion, password=password)
        usuario.is_admin = True
        usuario.save(using=self._db)

        return usuario


class Usuario(AbstractBaseUser):
    ci = models.CharField('Identificación', max_length=9, unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    profesion = models.CharField(max_length=30)
    is_active = models.BooleanField('Activo', default=True)
    is_admin = models.BooleanField('Administrador', default=False)

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
