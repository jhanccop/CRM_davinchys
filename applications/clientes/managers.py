from django.db import models

class ContactManager(models.Manager):
    def search_contact(self, WellName):
        result = self.filter(
            PumpName=WellName
        ).values("id").first()
        return result

class ClientManager(models.Manager):
    def listar_clientes(self):
        return self.all().order_by('-businessName')