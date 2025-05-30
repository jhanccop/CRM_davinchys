from django.db import models

from .managers import ClientManager #ContactManager

class Contacto(models.Model):
    """
        Contacto de compañia cliente
    """
    full_name = models.CharField(
        'Nombres', 
        max_length=30
    )

    last_name = models.CharField(
        'Apellidos', 
        max_length=30
    )

    email = models.EmailField(unique = True)
    phoneNumber = models.CharField('Telefono',blank = True, null=True)

    #objects = ContactManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name
    
    def __str__(self):
        return self.full_name

class Cliente(models.Model):

     # idioma de contrato
    ESP = '0'
    ENG = '1'
    OTRO = '1'
    
    LANGUAGE_CHOISES = [
            (ESP, "Español"),
            (ENG, "Ingles"),
            (OTRO, "Otro"),
        ]
    

    # tipo de cliente
    CLIENTE = '0'
    PROVEEDOR = '1'
    
    CLIENT_CHOISES = [
            (CLIENTE, "cliente"),
            (PROVEEDOR, "proveedor"),
        ]
    
    # Canal de captación:
    DIRECTO = '0'
    PARTNER = '1'
    LICITACION = '2'
    OTRO = '3'
    
    CHANNEL_CHOISES = [
            (DIRECTO, "Directo"),
            (PARTNER, "Partner"),
            (LICITACION, "Licitación"),
            (OTRO, "Otro"),
        ]
    
    # ORIGEN
    NACIONAL = '0'
    EXTRANGERO = '1'
    
    LOCATION_CHOISES = [
            (NACIONAL, "nacional"),
            (EXTRANGERO, "extrangero"),
        ]
    
    tradeName = models.CharField('Razon Social',blank = True, null=True)
    ruc = models.CharField('RUC - DNI',blank = True, null=True, unique=True)
    locationClient = models.CharField(
        'Por origen',
        max_length=1, 
        choices=LOCATION_CHOISES,
        null=True,
        blank=True
    )
    country = models.CharField('País',blank = True, null=True)
    brandName = models.CharField('Marca',blank = True, null=True)

    typeClient = models.CharField(
        'Categoria',
        max_length=1, 
        choices=CLIENT_CHOISES,
        null=True,
        blank=True
    )

    channel = models.CharField(
        'Canal de captación',
        max_length=1, 
        choices=CHANNEL_CHOISES,
        null=True,
        blank=True
    )

    contact = models.OneToOneField(Contacto, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    phoneNumber = models.CharField('Telefono',blank = True, null=True)
    webPage = models.CharField('Página Web',blank = True, null=True)
    email = models.EmailField(blank = True, null=True)

    languageContract = models.CharField(
        'Idioma de contrato',
        max_length=1, 
        choices=LANGUAGE_CHOISES,
        null=True,
        blank=True
    )

    legalJurisdiction = models.BooleanField("Jurisdicción legal aplicable",default=True,blank = True, null=True)
    internationalBilling = models.BooleanField("Facturación internacional",default=True,blank = True, null=True)
    electronicSignature = models.BooleanField("Firma electrónica",default=False,blank = True, null=True)

    objects = ClientManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.tradeName
    
    class Meta:
        ordering = ['tradeName']
    
    def __str__(self):
        return f"[{self.ruc}] {self.tradeName}"
    
class CuentasBancarias(models.Model):
    """
        Contacto de compañia cliente
    """
     # Bancos
    BCP = '0'
    BBVA = '1'
    INTERBANK = '2'
    SCOTIABANK = '3'
    COMERCIO = '4'
    BANBIF = '5'
    PICHINCHA = '6'
    GNB = '7'
    MIBANCO = '8'
    FALABELLA = '9'
    CITIBANK = '10'
    RIPLEY = '11'
    
    BANK_CHOICES = [
            (BCP, "BCP"),
            (BBVA, "BBVA"),
            (INTERBANK, "INTERBANK"),
            (SCOTIABANK, "SCOTIABANK"),
            (COMERCIO, "COMERCIO"),
            (BANBIF, "BANBIF"),
            (PICHINCHA, "PICHINCHA"),
            (GNB, "GNB"),
            (MIBANCO, "MIBANCO"),
            (FALABELLA, "FALABELLA"),
            (CITIBANK, "CITIBANK"),
            (RIPLEY, "RIPLEY"),
        ]

    bankName = models.CharField(
        'Banco',
        max_length=2, 
        choices=BANK_CHOICES,
        null=True,
        blank=True
    )

    # MONEDA
    SOLES = '0'
    DOLARES = '1'
    EUROS = '2'

    TYPE_CURRENCY_CHOISES = [
        (SOLES, "S/."),
        (DOLARES, "$"),
        (EUROS, "€"),
    ]

    typeCurrency = models.CharField(
        'Tipo de moneda',
        max_length=1, 
        choices = TYPE_CURRENCY_CHOISES,
        null=True,
        blank=True
    )

    # TIPO DE CUENTA
    AHORROS = '0'
    CORRIENTE = '1'
    SUELDO = '2'
    AHORROSJSAT = '3'
    AHORROSDAV = '4'

    TYPE_ACCOUNT_CHOISES = [
        (AHORROS, "Ahorros"),
        (CORRIENTE, "Corriente"),
        (SUELDO, "Sueldo"),
        (AHORROSJSAT, "Ahorros JSAT"),
        (AHORROSDAV, "Ahorros DAVINCHY"),
    ]

    typeAccount = models.CharField(
        'Tipo de cuenta',
        max_length=1, 
        choices = TYPE_ACCOUNT_CHOISES,
        null=True,
        blank=True
    )

    idClient = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True, related_name="CuentaBancariaCliente")
    
    account = models.CharField('Nro Cuenta',blank = True, null=True)
    accountCCI = models.CharField('Nro CCI',blank = True, null=True)

    def get_short_name(self):
        return self.bankName
    
    def get_full_name(self):
        return self.account
    
    def __str__(self):
        return f"[{self.idClient}] {self.get_bankName_display()} {self.get_typeCurrency_display()} {self.account}"