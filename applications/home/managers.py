from django.db import models

class ContainerTrackingManager(models.Manager):
    def searchOrder(self, order):
       return self.filter(trackingNumber = order)