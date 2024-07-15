from django.db import models

class WorkerManager(models.Manager):
    def listar_personal(self):
        return self.all().order_by('-full_name')