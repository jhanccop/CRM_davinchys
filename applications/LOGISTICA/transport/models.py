from model_utils.models import TimeStampedModel
from django.db import models

from applications.COMERCIAL.purchase.models import requirements


from .managers import (
    ContainerManager,
)

class Container(TimeStampedModel): 
    """ Contenedores """
    from applications.COMERCIAL.sales.models import quotes
    idQuote = models.ForeignKey(quotes, on_delete=models.CASCADE, null=True, blank=True)
    idRequirement = models.ForeignKey(requirements, on_delete=models.CASCADE, null=True, blank=True)
    
    containerName = models.CharField(
        "Nombre de contenedor",
        max_length = 100,
        null=True,
        blank=True
    )

    shortDescription = models.TextField(
        'Descripción corta',
        null = True,
        blank = True
    )

    objects = ContainerManager()

    class Meta:
        ordering = ['created']
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'

    def __str__(self):
        return f" CON - {self.id} | {self.idQuote}"
