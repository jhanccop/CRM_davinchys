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
    # tipo de cliente
    CLIENTE = '0'
    PROVEEDOR = '1'
    
    CLIENT_CHOISES = [
            (CLIENTE, "cliente"),
            (PROVEEDOR, "proveedor"),
        ]
    
    # tipo de cliente por ubicacion
    NACIONAL = '0'
    EXTRANGERO = '1'
    
    LOCATION_CHOISES = [
            (NACIONAL, "nacional"),
            (EXTRANGERO, "extrangero"),
        ]
    
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

    tradeName = models.CharField('Razon Social',blank = True, null=True)
    ruc = models.CharField('RUC - DNI',blank = True, null=True)
    brandName = models.CharField('Marca',blank = True, null=True)
    city = models.CharField('Ciudad',blank = True, null=True)
    phoneNumber = models.CharField('Telefono',blank = True, null=True)
    contact = models.OneToOneField(Contacto, on_delete=models.CASCADE, null=True, blank=True, unique=True)
    webPage = models.CharField('Página Web',blank = True, null=True)
    email = models.EmailField(unique = True,blank = True, null=True)
    bankName = models.CharField(
        'Banco',
        max_length=2, 
        choices=BANK_CHOICES,
        null=True,
        blank=True
    )
    account = models.CharField('Nro Cuenta',blank = True, null=True)

    typeClient = models.CharField(
        'Categoria',
        max_length=1, 
        choices=CLIENT_CHOISES,
        null=True,
        blank=True
    )

    locationClient = models.CharField(
        'Por origen',
        max_length=1, 
        choices=LOCATION_CHOISES,
        null=True,
        blank=True
    ) 

    objects = ClientManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.tradeName
    
    def __str__(self):
        return f"[{self.ruc}] {self.tradeName} {self.account}"