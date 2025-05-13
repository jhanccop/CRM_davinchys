from django.db import models

from model_utils.models import TimeStampedModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager, DocsManager

class User(AbstractBaseUser, PermissionsMixin):
    # TIPO DE USUARIOS
    ADMINISTRADOR = '0' # Joel, Gustavo, Jesus
    CONTABILIDAD = '1' # Keren
    SUPERVISOR_PRODUCCION = '2'
    SUPERVISOR_COMPRAS = '3'
    TRABAJADOR = '4'
    ADQUISICIONES = '5' # Jose
    FINANZAS = '6' # Gustavo
    TESORERIA = '7'
    CONSULTOREXTERNO = '8'
    RECURSOSHUMANOS = '9'
    
    #
    ROLES_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (CONTABILIDAD, 'Contabilidad'),
        (SUPERVISOR_PRODUCCION, 'Supervisor producción'),
        #(SUPERVISOR_COMPRAS, 'Supervisor compras'),
        (TRABAJADOR, 'Trabajador'),
        (ADQUISICIONES, 'Adquisiciones'),
        (FINANZAS, 'Finanzas'),
        (TESORERIA, 'Tesoreria'),
        (CONSULTOREXTERNO, 'Consultor'),
        (RECURSOSHUMANOS, 'Recursos humanos'),
    ]

    # GENEROS
    VARON = 'M'
    MUJER = 'F'

    GENDER_CHOICES = [
        (VARON, 'Masculino'),
        (MUJER, 'Femenino'),
    ]

    # CONDICIONES
    ACTIVO = "0"
    CESADO = "1"
    LICENCIA = "2"
    VACACIONES = "3"

    CONDITIONS_CHOICES = [
        (ACTIVO, 'Activo'),
        (CESADO, 'Cesado'),
        (LICENCIA, 'Licencia'),
        (VACACIONES, 'Vacaciones'),
    ]

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique = True)
    full_name = models.CharField('Nombres', max_length=100)
    last_name = models.CharField('Apellidos', max_length=100, blank=True, null=True)
    phoneNumber = models.CharField('Telefono',blank = True, null=True)
    ruc = models.CharField('RUC',blank = True, null=True)
    dni = models.CharField('DNI',blank = True, null=True)
    address = models.CharField('Direccion',blank = True, null=True)

    position = models.CharField(
        'Tipo de usuario',
        max_length=1, 
        choices=ROLES_CHOICES, 
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

    # CONTACTO DE EMERGENCIA
    EC_full_name = models.CharField('Contacto - nombres', max_length=100,blank = True, null=True)
    EC_relationship = models.CharField('Contacto - parentesco', max_length=20,blank = True, null=True)
    EC_phone = models.CharField('Contacto - telefono', max_length=20,blank = True, null=True)
    EC_email = models.EmailField('Contacto - correo',blank = True, null=True)

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

class Documentations(TimeStampedModel):
    
    # CONDICIONES
    CONTRATO = "0"
    CV = "1"
    INFORMEMENSUAL = "2"
    MEMORANDUM = "3"
    OFICIO = "4"
    CARTA = "5"
    OTRO = "6"
    DNI = "7"

    TYPE_CHOICES = [
        (CONTRATO, 'Contrato'),
        (CV, 'CV'),
        (INFORMEMENSUAL, 'Informe Mensual'),
        (MEMORANDUM, 'Memorandum'),
        (OFICIO, 'Oficio'),
        (CARTA, 'Carta'),
        (OTRO, 'Otro'),
        (DNI, 'DNI'),
    ]

    id = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="person")
    
    typeDoc = models.CharField(
        'Tipo de dpcumento',
        max_length=1,
        choices=TYPE_CHOICES,
        #unique=True
    )
    idDoc = models.CharField('Id doc',max_length=25,null=True,blank=True)
    sumary = models.CharField('Resumen',max_length=150,null=True,blank=True)
    is_multiple = models.BooleanField(default=False)

    doc_file = models.FileField(upload_to='doc_pdfs/',null=True,blank=True)

    objects = DocsManager()

    def delete(self, *args, **kwargs):
        self.doc_file.delete()
        super(Documentations, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Documento de personal'
        verbose_name_plural = 'Documentos de personal'
    
    def __str__(self):
        return f"{str(self.idUser)} | {str(self.get_typeDoc_display())}"

