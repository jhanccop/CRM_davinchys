from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    # TIPO DE USUARIOS
    ADMINISTRADOR = '0'
    CONTABILIDAD = '1'
    SUPERVISOR_PRODUCCION = '2'
    SUPERVISOR_COMPRAS = '3'
    TRABAJADOR = '4'
    ADQUISICIONES = '5'
    FINANZAS = '6'
    TESORERIA = '7'
    
    #
    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (CONTABILIDAD, 'Contabilidad'),
        (SUPERVISOR_PRODUCCION, 'Supervisor producción'),
        (SUPERVISOR_COMPRAS, 'Supervisor compras'),
        (TRABAJADOR, 'Trabajador'),
        (ADQUISICIONES, 'Adquisiciones'),
        (FINANZAS, 'Finanzas'),
        (TESORERIA, 'Tesoreria'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique = True)
    full_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100, blank=True, null=True)

    position = models.CharField(
        'Tipo de usuario',
        max_length=1, 
        choices=ROLES_CHOICES, 
        blank=True
    )

    #
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def __str__(self):
        return str(self.full_name)
