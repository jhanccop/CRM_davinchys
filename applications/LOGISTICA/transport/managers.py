from django.db import models
from datetime import timedelta, datetime

from django.db.models import OuterRef, Subquery

class ContainerManager(models.Manager):
    def ListaContenedoresPorRuc(self,intervalo,idTin):
        """
            Lista de CONTAINER
        """
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]

        # =========== Creacion de rango de fechas ===========
        rangeDate = [intervals[0] - timedelta(days = 1),None]
        
        if len(intervals) == 1:
            rangeDate[1] = intervals[0] + timedelta(days = 1)
        else:
            rangeDate[1] = intervals[1] + timedelta(days = 1)

        result = self.filter(
            created__range=rangeDate,
            idPetitioner__company__id = idTin
        )
        return result

    
    