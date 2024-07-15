from django.db import models

from model_utils.models import TimeStampedModel

class Workers(TimeStampedModel):
    
    # AREAS
    DIRECCION = '0'
    ADMINISTRACION = '1'
    VENTAS = '2'
    PRODUCCION = '3'
    CONTABILIDAD = '4'
    DESARROLLO = '5'

    # GENEROS
    VARON = 'M'
    MUJER = 'F'

    # CONDICIONES
    ACTIVO = "0"
    CESADO = "1"
    LICENCIA = "2"
    VACACIONES = "3"

    # TIPO DE MONEDA
    SOLES = "0"
    DOLARES = "1"

    AREAS_CHOICES = [
        (DIRECCION, 'Direccion'),
        (ADMINISTRACION, 'Administracion'),
        (VENTAS, 'Ventas'),
        (PRODUCCION, 'Produccion'),
        (CONTABILIDAD, 'Contabilidad'),
        (DESARROLLO, 'Desarrollo'),
    ]

    GENDER_CHOICES = [
        (VARON, 'Masculino'),
        (MUJER, 'Femenino'),
    ]

    CONDITIONS_CHOICES = [
        (ACTIVO, 'Activo'),
        (CESADO, 'Cesado'),
        (LICENCIA, 'Licencia'),
        (VACACIONES, 'Vacaciones'),
    ]

    CURRENCY_CHOISES = [
        (SOLES, "Soles"),
        (DOLARES, "Dolares")
    ]

    full_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100, blank=True, null=True)
    email = models.EmailField(unique = True)
    phoneNumber = models.CharField('Telefono',blank = True, null=True)

    area = models.CharField(
        'Area en la Empresa',
        max_length=1, 
        choices=AREAS_CHOICES, 
        blank=True
    )

    gender = models.CharField(
        'Género',
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True
    )

    condition = models.CharField(
        'Condicion',
        max_length=1, 
        choices=CONDITIONS_CHOICES, 
        blank=True
    )

    currency = models.CharField(
        "Tipo de moneda de remuneracion",
        max_length=1, 
        choices=CURRENCY_CHOISES, 
        blank=True
    )

    salary = models.DecimalField(
        'Salario mensual',
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )

    date_entry = models.DateField(
        'Fecha de contratacion', 
        blank=True,
        null=True
    )

    date_termination = models.DateField(
        'Fecha de cese', 
        blank=True,
        null=True
    )

    #objects = WorkersManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'

    def __str__(self):
        return self.full_name
    