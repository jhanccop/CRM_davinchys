from django.db import models

class AccountManager(models.Manager):
    """ procedimiento para listar cuentas """
    
    def listarcuentas(self):
        return self.all()
    
    def ListaCuentasGeneral(self,moneda,cajaChica):
        return self.filter(currency = moneda,cajaChica=cajaChica).order_by("id")
    
    def CuentasById(self,id):
        return self.get(id = id)
    
    def CuentasByLastUpdate(self):
        return self.all().order_by("modified").last()
    
    def CuentasByNumber(self,number):
        return self.get(accountNumber = number)
    
    def CuentasByCajaChica(self,cajaChica):
        return self.filter(cajaChica = cajaChica).order_by("id")