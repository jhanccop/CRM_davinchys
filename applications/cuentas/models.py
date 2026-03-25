# third-party
from model_utils.models import TimeStampedModel
from django.db.models.signals import post_save

# Django
from django.db import models

from .managers import AccountManager, TinManager

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
    HOLDING = '0'
    SUBSIDIARY = '1'

    COMPANY_TYPE_CHOICES = [
        (HOLDING, 'Holding'),
        (SUBSIDIARY, 'Subsidiaria'),
    ]

    company_type = models.CharField(max_length=1, choices=COMPANY_TYPE_CHOICES, null=True, blank=True)

    #objects = TinManager()

    class Meta:
        verbose_name = 'Ruc'
        verbose_name_plural = 'Rucs'

    def __str__(self):
        return f"{self.tin} / {self.tinName}"

class Account(TimeStampedModel):

    CURRENCY_CHOICES = [
            ("0", "PEN"),
            ("1", "USD"),
            ("2", "EUR")
        ]
    
    accountName   = models.CharField('Nombre de cuenta', max_length=50)
    nickName      = models.CharField('Nombre corto', max_length=10, blank=True, null=True)
    accountNumber = models.CharField('Número de cuenta', max_length=30, unique=True)
    bankName      = models.CharField('Banco', max_length=50)
    idTin         = models.ForeignKey(Tin, on_delete=models.CASCADE, null=True, blank=True, related_name='accounts', verbose_name='Empresa')
    initialAccount= models.DecimalField('Saldo inicial', max_digits=14, decimal_places=2, blank=True, null=True)
    initalDate    = models.DateTimeField('Fecha inicial')
    currency      = models.CharField('Moneda', max_length=1, choices=CURRENCY_CHOICES, blank=True)
    description   = models.TextField('Descripción', blank=True)
    state         = models.BooleanField('Activo', default=True)
    cajaChica     = models.BooleanField('Caja chica', default=False, blank=True, null=True)
    objects = AccountManager()
 
    class Meta:
        verbose_name        = 'Cuenta bancaria'
        verbose_name_plural = 'Cuentas bancarias'
        ordering            = ['idTin__tinName', 'accountName']
 
    def __str__(self):
        return f"[{self.nickName}] {self.accountNumber}"
 
    @property
    def currency_label(self):
        return dict(CURRENCY_CHOICES).get(self.currency, self.currency)

    
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