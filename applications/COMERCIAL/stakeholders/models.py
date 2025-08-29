from django.db import models

class supplierContact(models.Model):
    """
        Contacto de compañia proveedores
    """
    name = models.CharField(
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
        return self.name
    
    def __str__(self):
        return self.name

class supplier(models.Model):
    """ Supplier """

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
    numberIdSupplier = models.CharField('Numero de proveedor',blank = True, null=True, unique=True)
    typeDocument = models.CharField(
        'Tipo de documento',
        max_length=1, 
        choices=TYPE_DOCUMENT_CHOICES,
        null=True,
        blank=True
    )

    location = models.CharField(
        'Por origen',
        max_length=1, 
        choices=LOCATION_CHOISES,
        null=True,
        blank=True
    )

    status = models.CharField(
        'Estado Proveedor',
        max_length=1, 
        choices = STATUS_CHOISES,
        default = NO_ACTIVO,
        null=True,
        blank=True
    )

    country = models.CharField('País',blank = True, null=True)
    brandName = models.CharField('Marca',blank = True, null=True)

    contact = models.OneToOneField(supplierContact, on_delete=models.CASCADE, null=True, blank=True, related_name = "supplier_contact")

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
        return f"{self.numberIdSupplier} - {self.tradeName}"

class clientContact(models.Model):
    """
        Contacto de compañia cliente
    """
    name = models.CharField(
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
        return self.name
    
    def __str__(self):
        return self.name

class client(models.Model):
    """ Clients """

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
    
    # ==================== CAMPOS DE MODELO ====================

    tradeName = models.CharField('Razon Social',blank = True, null=True)
    numberIdClient = models.CharField('Número de Id de cliente',blank = True, null=True, unique=True)
    typeDocument = models.CharField(
        'Tipo de documento',
        max_length=1, 
        choices=TYPE_DOCUMENT_CHOICES,
        null=True,
        blank=True
    )
    location = models.CharField(
        'Por origen',
        max_length=1, 
        choices=LOCATION_CHOISES,
        null=True,
        blank=True
    )
    status = models.CharField(
        'Estado cliente',
        max_length=1, 
        choices=STATUS_CHOISES,
        default=NO_ACTIVO,
        null=True,
        blank=True
    )

    country = models.CharField('País',blank = True, null=True)
    brandName = models.CharField('Marca',blank = True, null=True)

    contact = models.OneToOneField(clientContact, on_delete=models.CASCADE, null=True, blank=True, unique=True)

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
        return f"{self.numberIdClient} - {self.tradeName}"

class bankAccountsClient(models.Model):
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
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
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

    idClient = models.ForeignKey(client, on_delete=models.CASCADE, null=True, blank=True, related_name="CuentaBancariaCliente")
    
    account = models.CharField('Nro Cuenta',blank = True, null=True)
    accountCCI = models.CharField('Nro CCI',blank = True, null=True)

    def get_short_name(self):
        return self.bankName
    
    def get_full_name(self):
        return self.account
    
    def __str__(self):
        return f"[{self.idClient}] {self.get_bankName_display()} {self.get_typeCurrency_display()} {self.account}"

class bankAccountsSupplier(models.Model):
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
        (SOLES, "PEN"),
        (DOLARES, "USD"),
        (EUROS, "EUR"),
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

    idSupplier = models.ForeignKey(supplier, on_delete=models.CASCADE, null=True, blank=True, related_name="CuentaBancariaCliente")
    
    account = models.CharField('Nro Cuenta',blank = True, null=True)
    accountCCI = models.CharField('Nro CCI',blank = True, null=True)

    def get_short_name(self):
        return self.bankName
    
    def get_full_name(self):
        return self.account
    
    def __str__(self):
        return f"[{self.idSupplier}] {self.get_bankName_display()} {self.get_typeCurrency_display()} {self.account}"
