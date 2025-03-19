from django.db import models
from model_utils.models import TimeStampedModel

from .managers import ContainerTrackingManager

class ContainerTracking(TimeStampedModel):
    STARTPO = "0"
    SEATRAVEL = "1"
    LANDTRAVEL = "2"
    ARRIVALGREENVILLE = "3"
    DELIVERYGREENVILLEASPO = "4"

    STATUS_CHOICES = (
        (STARTPO, 'Start as per the PO'),
        (SEATRAVEL, 'Sea Travel'),
        (LANDTRAVEL, 'Land Travel'),
        (ARRIVALGREENVILLE, 'Delivery in Greenville as per PO'),
        (DELIVERYGREENVILLEASPO, 'Perdido'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default='0',
        null=True,
        blank=True)
    
    id = models.AutoField(primary_key=True)
    trackingNumber = models.CharField(
        'Seguimiento',
        max_length = 20,
        null=True,
        blank=True,
        unique=True
    )

    pdf_file = models.FileField(upload_to='doc_pdfs/',null=True,blank=True)

    objects = ContainerTrackingManager()

    def delete(self, *args, **kwargs):
        self.pdf_file.delete()
        super(ContainerTracking, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Numero de seguimiento'
        verbose_name_plural = 'Numeros de seguimientos'

    def __str__(self):
        return f"{self.trackingNumber}"