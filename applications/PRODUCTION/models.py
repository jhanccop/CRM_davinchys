from model_utils.models import TimeStampedModel

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

from applications.COMERCIAL.stakeholders.models import supplier 

class Trafos(TimeStampedModel):
    """
        Catalogo de Transformadores
    """

    idUser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        blank=True, 
        null=True
    )

    id = models.AutoField(primary_key=True)

    idSupplier = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True,related_name="prod_trafo_supplier")
    
    # ========== KVA ==========
    KVA_CHOICES = (
        ('0', '75'),
        ('1', '100'),
        ('2', '150'),
        ('3', '167'),
        ('4', '225'),
        ('5', '250'),
        ('6', '300'),
        ('7', '500'),
        ('8', '750'),
        ('9', '1000'),
        ('10', '1500'),
        ('11', '2000'),
        ('12', '2000/3000'),
        ('13', '2500'),
        ('14', '2600'),
        ('15', '3000'),
        ('16', '3000/3750'),
        ('17', '3750'),
        ('18', '5000'), 
    )
    KVA = models.CharField(
        'kVA CAPACITY',
        max_length=2,
        choices=KVA_CHOICES,
        blank=True, 
        null=True
    )

    # ========== HIGH VOLTAGE ==========
    HV_CHOICES = (
        ('0', '4160'),
        ('1', '7200'),
        ('2', '8320'),
        ('3', '12470'),
        ('4', '13200'),
        ('5', '13800'),
        ('6', '14400'),
        ('7', '21600'),
        ('8', '22860'),
        ('9', '23960'),
        ('10', '24940'),
        ('11', '34500'),
    )
    HV = models.CharField(
        'HV',
        max_length=2,
        choices=HV_CHOICES,
        blank=True, 
        null=True
    )

    # ========== LOW VOLTAGE ==========
    LV_CHOICES = (
        ('0', '240/120'),
        ('1', '480Y/277'),
        ('2', '208Y/120'),
        ('3', '4160Y/2400'),
        ('4', '277/480Y'),
    )
    LV = models.CharField(
        'LV',
        max_length=2,
        choices=LV_CHOICES,
        blank=True, 
        null=True
    )

    # ========== FREQUENCY ==========
    HZ_CHOICES = (
        ('0', '50'),
        ('1', '60'),
    )

    HZ = models.CharField(
        'HZ',
        max_length=2,
        choices=HZ_CHOICES,
        blank=True, 
        null=True
    )

    # ========== PHASE ==========
    MONO = "0"
    THREE = "1"
    PHASE_CHOICES = (
        (MONO, 'Mono-phasic'),
        (THREE, 'Three-phasic'),
    )
    PHASE_NICK = {
        MONO: 'MO',
        THREE: 'TP',
    }
    PHASE = models.CharField(
        'PHASE',
        max_length=2,
        choices=PHASE_CHOICES,
        blank=True, 
        null=True
    )

    # ========== DERIVATIONS ==========
    TAPS = "0"
    KTAPS = "1"
    DERIVATIONS_CHOICES = (
        (TAPS, 'TAPS'),
        (KTAPS, 'KTAPS'),
    )
    DERIVATIONS = models.CharField(
        'Derivations',
        max_length=2,
        choices=DERIVATIONS_CHOICES,
        blank=True, 
        null=True
    )

    KTAPSVALUES = ArrayField(
        models.IntegerField(),
        default=list,
        blank=True,
        null=True
    )

    # ==== MOUNTING ====
    POLE = "0"
    PEDESTAL = "1"
    PLATFORM = "2"
    UNDERGROUND = "3"
    SUBSTATION = "4"

    MOUNTING_CHOICES = (
        (POLE, 'Pole'),
        (PEDESTAL, 'Pedestal'),
        (PLATFORM, 'Platform'),
        (UNDERGROUND, 'Underground'),
        (SUBSTATION, 'Substation'),
    )
    
    MOUNTING_NICK = {
        POLE: 'PM',
        PEDESTAL: 'PED',
        PLATFORM: 'PLA',
        UNDERGROUND: 'UND',
        SUBSTATION: 'SUB',
    }

    MOUNTING = models.CharField(
        'MOUNTING TYPE',
        max_length=2,
        choices=MOUNTING_CHOICES,
        blank=True, 
        null=True
    )

    # ==== COOLING ====
    ONAN = "0"
    ONAF = "1"
    KNAN = "2"
    KNAF = "3"
    AN = "4"
    AF = "5"
    OFAN = "6"
    OFAF = "7"
    ONWF = "8"
    OFWF = "9"

    COOLING_CHOICES = (
        (ONAN, 'ONAN'),
        (ONAF, 'ONAF'),
        (KNAN, 'KNAN'),
        (KNAF, 'KNAF'),
        (AN, 'AN'),
        (AF, 'AF'),
        (OFAN, 'OFAN'),
        (OFAF, 'OFAF'),
        (ONWF, 'ONWF'),
        (OFWF, 'OFWF'),
    )

    COOLING = models.CharField(
        'COOLING',
        max_length=2,
        choices=COOLING_CHOICES,
        blank=True, 
        null=True
    )

    # ==== WINDING ====
    WINDING_CHOICES = (
        ('0', 'Al'),
        ('1', 'Cu'),
    )

    WINDING = models.CharField(
        'WINDING',
        max_length=2,
        choices=WINDING_CHOICES,
        blank=True, 
        null=True
    )

    # ==== CONNECTION ====
    CONNECTION_CHOICES = (
        ('0', 'Dyn1'),
        ('1', 'Dyn11'),
        ('2', 'Yyn0'),
        ('3', 'YNyn0'),
        ('4', 'Dzn0'),
        ('5', 'Yd11'),
        ('6', 'lio'),
    )
    CONNECTION = models.CharField(
        'CONNECTION',
        max_length=2,
        choices=CONNECTION_CHOICES,
        blank=True, 
        null=True
    )

    # ==== STANDARD ====
    STANDARD_CHOICES = (
        ('0', 'IEEE C57.12.00'), # subestaciones
        ('1', 'IEEE C57.12.20'), # monofasicos aéreos
        ('2', 'IEEE C57.12.21'), # monofasicos tipo pedestal
        ('3', 'IEEE C57.12.34'), # pedestales
    )

    STANDARD = models.CharField(
        'STANDARD',
        max_length=2,
        choices=STANDARD_CHOICES,
        blank=True, 
        null=True
    )

    #objects = TrafosManager()

    class Meta:
        verbose_name = 'Catalogo de transformadores'
        verbose_name_plural = 'Transformadores'

    def __str__(self):
        return f"{self.PHASE_NICK.get(self.PHASE, '')}{self.MOUNTING_NICK.get(self.MOUNTING, '')}{self.get_KVA_display()}"
