# third-party
from model_utils.models import TimeStampedModel
from django.db.models.signals import post_save

# Django
from django.db import models

from .managers import AccountManager

from .signals import (
  update_accounts,
)

class Tin(TimeStampedModel):
    tin = models.CharField(
        'RUC',
        max_length=50,
    )

    tinName = models.CharField(
        'Razón Social',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Ruc'
        verbose_name_plural = 'Rucs'

    def __str__(self):
        return f"{self.tin} / {self.tinName}"

class Account(TimeStampedModel):
    """
        Cuentas Bancarias
    """

    CURRENCY_CHOISES = [
            ("0", "S/."),
            ("1", "$")
        ]
    
    accountName = models.CharField(
        'Nombre de cuenta',
        max_length=50,
    )

    nickName = models.CharField(
        'Nombre cortp',
        max_length=10,
        blank=True,
        null=True
    )
    
    accountNumber = models.CharField(
        'Numero de cuenta',
        max_length=30,
        unique=True
    )

    bankName = models.CharField(
        'Nombre de banco',
        max_length=50,
    )

    idTin = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True)

    accountBalance = models.DecimalField(
        'Monto en sistema',
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )

    lastUpdateCRM = models.DateTimeField(
        'Actualización CRM',
    )

    currency = models.CharField(
        'Tipo de moneda',
        max_length=1, 
        choices=CURRENCY_CHOISES, 
        blank=True
    )

    description = models.TextField(
        'Descripcion',
        blank=True,
    )

    state = models.BooleanField(
        'Estado',
        default=True
    )

    cajaChica = models.BooleanField(
        'Caja Chica',
        default=False,
        blank=True,
        null=True
    )

    objects = AccountManager()

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas bancarias'

    def __str__(self):
        return f"[{self.nickName}] {self.accountNumber}"
    
class ManualAccount(TimeStampedModel):
    """
        Cuentas Bancarias Reales
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    idAcount = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="Account")

    realBalance = models.DecimalField(
        'Monto en cuenta',
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True
    )

    #objects = AccountManager()

    class Meta:
        verbose_name = 'Cuenta Manual'
        verbose_name_plural = 'Cuentas bancarias Manuales'

    def __str__(self):
        return 'Man ' + self.idAcount.accountName
    
post_save.connect(update_accounts, sender = ManualAccount)