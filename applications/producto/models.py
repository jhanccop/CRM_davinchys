# third-party
from model_utils.models import TimeStampedModel
# Django
from django.db import models
# local

from applications.clientes.models import Cliente
from applications.personal.models import Workers

from .managers import ProductManager

# ======================== TRANSFORMER ======================
class Transformer(TimeStampedModel):
    """
        Catalogo de Transformadores
    """

    KVA_CHOICES = (
        ('0', '15'),
        ('1', '30'),
        ('2', '75'),
        ('3', '100'),
        ('4', '167'),
        ('5', '200'),
        ('6', '250'),
        ('7', '400'),
        ('8', '500'),
        ('9', '600'),
        ('10', '750'),
        ('11', '1000'),
        ('12', '1500'),
        ('13', '2000'), 
    )

    HVTAP_CHOICES = (
        ('0', 'K-Tap - HV'),
        ('1', 'Fix HV'),
    )

    KTapHV_CHOICES = (
        ('0', '12700/7200'),
        ('1', '24940/14400'),
    )
    FIXHV_CHOICES = (
        ('0', '7200'),
        ('1', '12470'),
        ('2', '22900'),
    )

    LV_CHOICES = (
        ('0', '120/240'),
        ('1', '277/480'),
    )

    HZ_CHOICES = (
        ('0', '50'),
        ('1', '60'),
    )

    PHASE_CHOICES = (
        ('0', 'Mono-phasic'),
        ('1', 'Three-phasic'),
    )

    MOUNTING_CHOICES = (
        ('0', 'Pole'),
        ('1', 'Standard'),
        ('2', 'Feed Through Pad'),
    )

    COOLING_CHOICES = (
        ('0', 'Oil'),
        ('1', 'Dry'),
    )

    WINDING_CHOICES = (
        ('0', 'Al - Al'),
        ('1', 'Cu - CU'),
    )

    INSULAT_CHOICES = (
        ('0', 'A'),
        ('1', 'E'),
        ('2', 'H'),
    )

    CONNECTION_CHOICES = (
        ('0', 'WEY'),
        ('1', 'DELTA'),
    )

    STANDARD_CHOICES = (
        ('0', 'NMX-116'),
        ('1', 'IEC 61558'),
    )

    TENSION_CHOICES = (
        ('0', '220'),
        ('1', '380'),
        ('2', '400'),
        ('3', '460'),
        ('4', '600'),
        ('5', '10000'),
        ('6', '13800'),
        ('7', '20000'),
        ('8', '22900'),
    )

    TYPE_CHOICES = (
        ('0', 'Seco'),
        ('1', 'Aceite'),
        ('2', 'Pedestal'),
        ('3', 'Integrado'),
        ('4', 'Subestacion'),
        ('5', 'Poste'),
    )

    id = models.AutoField(primary_key=True)

    barcode = models.CharField(
        max_length = 100,
        unique=True,
        null=True,
        blank=True
    )

    provider = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE
    )

    model_name = models.CharField(
        "Modelo",
        max_length = 20,
        null=True,
        blank=True
    )

    KVA = models.CharField(
        'kVA CAPACITY',
        max_length=2,
        choices=KVA_CHOICES,
        blank=True, 
        null=True
    )

    HVTAP = models.CharField(
        'HV TAP',
        max_length=2,
        choices=HVTAP_CHOICES,
        blank=True, 
        null=True
    )

    KTapHV = models.CharField(
        'K Tap HV',
        max_length=2,
        choices=KTapHV_CHOICES,
        blank=True, 
        null=True
    )

    FIXHV = models.CharField(
        'FIX HV',
        max_length=2,
        choices=FIXHV_CHOICES,
        blank=True, 
        null=True
    )

    LV = models.CharField(
        'LV',
        max_length=2,
        choices=LV_CHOICES,
        blank=True, 
        null=True
    )

    HZ = models.CharField(
        'HZ',
        max_length=2,
        choices=HZ_CHOICES,
        blank=True, 
        null=True
    )

    TYPE = models.CharField(
        'TYPE',
        max_length=2,
        choices=PHASE_CHOICES,
        blank=True, 
        null=True
    )

    MOUNTING = models.CharField(
        'MOUNTING TYPE',
        max_length=2,
        choices=MOUNTING_CHOICES,
        blank=True, 
        null=True
    )

    COOLING = models.CharField(
        'COOLING',
        max_length=2,
        choices=COOLING_CHOICES,
        blank=True, 
        null=True
    )

    WINDING = models.CharField(
        'WINDING',
        max_length=2,
        choices=WINDING_CHOICES,
        blank=True, 
        null=True
    )

    INSULAT = models.CharField(
        'INSULAT CLASS',
        max_length=2,
        choices=INSULAT_CHOICES,
        blank=True, 
        null=True
    )

    CONNECTION = models.CharField(
        'CONNECTION',
        max_length=2,
        choices=CONNECTION_CHOICES,
        blank=True, 
        null=True
    )

    STANDARD = models.CharField(
        'STANDARD',
        max_length=2,
        choices=STANDARD_CHOICES,
        blank=True, 
        null=True
    )

    description = models.TextField(
        'Descripcion',
        blank=True,
        null=True,
    )

    #objects = TransformerManager()

    class Meta:
        verbose_name = 'Transformador'
        verbose_name_plural = 'Transformadores'

    def __str__(self):
        return 'TR [' + str(self.model_name) + ']'
    
# ======================== INVENTARIO ======================
class Inventario(TimeStampedModel):
    UNIT_CHOICES = (
        ('0', 'Unidades'),
        ('1', 'Kg'),
        ('2', 'Litros'),
    )

    STATUS_CHOICES = (
        ('0', 'Activo'),
        ('1', 'De baja'),
        ('2', 'Mantenimiento'),
        ('3', 'No habido'),
    )

    LOCATION_CHOICES = (
        ('0', 'Oficina Lima'),
        ('1', 'Usa'),
    )

    id = models.AutoField(primary_key=True)

    name = models.CharField(
        'Nombre', 
        max_length=40
    )

    brand = models.CharField(
        'Marca', 
        max_length=40,
        blank=True, 
        null=True
    )

    user = models.ForeignKey(
        Workers, 
        on_delete=models.CASCADE
    )

    code = models.CharField(
        "Codigo",
        max_length=13,
    )

    dateInput = models.DateField(
        'Fecha de adquisición',
        blank=True, 
        null=True
    )

    date = models.DateField(
        'Fecha',
        blank=True, 
        null=True
    )

    amount = models.IntegerField(
        'Cantidad',
        blank=True, 
        null=True
    )

    unit = models.CharField(
        'Unidad de medida',
        max_length=1,
        choices=UNIT_CHOICES, 
    )

    status = models.CharField(
        'Estado',
        max_length=1,
        choices=STATUS_CHOICES, 
    )

    location = models.CharField(
        'Ubicación',
        max_length=1,
        choices=LOCATION_CHOICES,
        blank=True, 
        null=True
    )

    verbose_name = 'Inventario'
    verbose_name_plural = 'Inventario'

    def __str__(self):
        return self.name
