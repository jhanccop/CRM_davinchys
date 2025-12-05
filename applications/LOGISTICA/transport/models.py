from model_utils.models import TimeStampedModel
from django.db import models
from django.conf import settings

from .managers import ContainerManager

# ================== CONTENEDORES ==================
class Container(TimeStampedModel):
    idPetitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,related_name="logistic_user")

    containerName = models.CharField(
        'Nombre',
        max_length = 50, 
        null = True,
        blank = True
    )

    # === CATEGORIA MONEDA ====
    PEN = '0'
    USD = '1'
    EUR = '2'

    CURRENCY_CHOICES = [
        (PEN,'PEN'),
        (USD,'USD'),
        (EUR,'EUR'),
    ]

    currency = models.CharField(
        'Moneda',
        max_length = 1, 
        choices = CURRENCY_CHOICES,
        null = True,
        blank = True
    )

    grossAmount = models.DecimalField(
        'Monto bruto', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    taxes = models.DecimalField(
        'Impuestos', 
        max_digits=10, 
        decimal_places=2,
        default=0,
        null = True,
        blank = True
    )

    netAmount = models.DecimalField(
        'Monto neto',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    isOrder = models.BooleanField("Es orden de compra?",default = False)

    shortDescription = models.CharField(
        'Descripción',
        max_length = 150,
        null = True, 
        blank = True,
    )

    objects = ContainerManager()

    def save(self, *args, **kwargs):
        # Calculamos automáticamente
        self.netAmount = self.grossAmount - self.taxes

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created']
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'

    def __str__(self):
        return f"{self.containerName}"

class ContainerTracking(TimeStampedModel):
    """ Modelo de seguimiento de requerimientos """
    # AREAS DE REQUERIMIENTO

    COMERCIAL = '1'
    FINANZAS = '2'
    PRODUCCION = '3'
    GERENCIA = '4'
    LOGISTICA = '5'

    AREAS_TRACKING_CHOICES = [
        (COMERCIAL, 'Comercial'),
        (FINANZAS, 'Finanzas'),
        (PRODUCCION, 'Producción'),
        (GERENCIA, 'Gerencia'),
        (LOGISTICA, 'Logistica'),
    ]

    # ESTADOS DE REQUERIMIENTO
    CREADO = '0'
    RECIBIDO = '1'
    APROBADO = '2'
    RECHAZADO = '3'
    OBSERVADO = '4'

    # ESTADO OREDEN DE COMPRA
    SOLICITADO = '5'    # APROBADA PPOR TODAS LAS INSTACIAS LISTAS PARA ADQUIRIR
    ENVIADOPROVEEDOR = '6'
    COTIZACIONRECIBIDA = '7'
    BIENPARCIALRECIBIDO = '8'
    BIENTOTALRECIBIDO = '9'
    FACTURADA = '10'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOPARCIAL = '10'      # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    PAGOTOTAL = '11'        # DERIVADA PARA SER PAGADA, ENTRA A LA LISTA DE CUENTAS POR PAGAR
    COMPLETADO = '12'
    
    STATE_CHOICES = [
        (CREADO, 'Creado'),
        (RECIBIDO, 'Recibido'),
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (OBSERVADO, 'Observado'),

        (SOLICITADO, 'Solicitado'),
        (ENVIADOPROVEEDOR, 'Enviado a proveedores'),
        (COTIZACIONRECIBIDA, 'Cotizado por proveedores'),
        (BIENPARCIALRECIBIDO, 'Parcailmente recepcionado'),
        (BIENTOTALRECIBIDO, 'Recepción total'),
        (FACTURADA, 'Facturado'),
        (PAGOPARCIAL, 'Pago parcial'),
        (PAGOTOTAL, 'Pagol total'),

        (COMPLETADO, 'Completado'),
    ]

    idContainer = models.ForeignKey(Container, on_delete = models.CASCADE, null=True, blank = True)

    status = models.CharField(
        'Estado de orden',
        max_length=2,
        choices=STATE_CHOICES,
        null = True,
        blank = True
    )

    area = models.CharField(
        'Area de seguimiento',
        max_length = 2, 
        choices = AREAS_TRACKING_CHOICES,
        null = True,
        blank = True
    )

    #objects = requestTrackingManager()

    class Meta:
        verbose_name = 'Tracking contenedor'
        verbose_name_plural = 'Tracking contenedores'
    
    def __str__(self):
        return f"{self.idContainer} | {self.get_area_display()} | {self.get_status_display()} "
