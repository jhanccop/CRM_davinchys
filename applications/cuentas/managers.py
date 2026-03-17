from django.db import models

class AccountManager(models.Manager):
    """ procedimiento para listar cuentas """
    
    def listarcuentas(self,compania_id):
        return self.filter(
            idTin__id = compania_id
        )
    
    def ListaCuentasGeneral(self,moneda,cajaChica):
        return self.filter(currency = moneda,cajaChica=cajaChica).order_by("id")
    
    def CuentasById(self,id):
        return self.get(id = id)
    
    def CuentasByLastUpdate(self, compania_id):
        return self.filter(
            idTin__id = compania_id
        ).order_by("modified").last()
    
    def CuentasByNumber(self,number):
        return self.get(accountNumber = number)
    
    def CuentasByCajaChica(self,cajaChica, idCompany):
        return self.filter(
            cajaChica = cajaChica,
            idTin = idCompany
        ).order_by("id")
    
    def for_tin(self, tin):
        return self.filter(idTin=tin, state=True)

    def active(self):
        return self.filter(state=True)

    def cajas_chicas(self):
        return self.filter(cajaChica=True, state=True)
    

class TinManager(models.Manager):
    def allCompanies(self):
        return self.all()