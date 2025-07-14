from django.db import models

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
        max_length = 50
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

class supplier(models.Model):
    """ Proveedor """

    # ORIGEN
    NACIONAL = '0'
    EXTRANGERO = '1'
    
    LOCATION_CHOISES = [
            (NACIONAL, "nacional"),
            (EXTRANGERO, "extrangero"),
        ]

    # STATUS SUPPLIER
    ACTIVO = '0'
    NO_ACTIVO = '1'
    
    STATUS_CHOISES = [
            (ACTIVO, "Activo"),
            (NO_ACTIVO, "No activo"),
        ]

    # TIPO DE DOCUMENTO
    RUC = '0'
    TIN = '1'
    DNI = '2'
    CE = '3'
    OTRO = '4'
    
    TYPE_DOCUMENT_CHOICES = [
            (RUC, "RUC"),
            (TIN, "TIN"),
            (DNI, "DNI"),
            (CE, "CE"),
            (OTRO, "OTRO"),
        ]
    
    tradeName = models.CharField('Razon Social',blank = True, null=True)
    idSupplier = models.CharField('Id de proveedor',blank = True, null=True, unique=True)
    typeDocument = models.CharField(
        'Tipo de documento',
        max_length=1, 
        choices=TYPE_DOCUMENT_CHOICES,
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

    status = models.CharField(
        'Estado Proveedor',
        max_length=1, 
        choices=STATUS_CHOISES,
        default=ACTIVO,
        null=True,
        blank=True
    )

    country = models.CharField('País',blank = True, null=True)
    brandName = models.CharField('Marca',blank = True, null=True)

    contact = models.OneToOneField(Contacto, on_delete=models.CASCADE, null=True, blank=True, unique=True)

    phoneNumber = models.CharField('Telefono',blank = True, null=True)
    webPage = models.CharField('Página Web',blank = True, null=True)
    email = models.EmailField(blank = True, null=True)

    #objects = supplierManager()

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.tradeName
    
    class Meta:
        ordering = ['tradeName']
    
    def __str__(self):
        return f"[{self.idSupplier}] {self.tradeName}"
    