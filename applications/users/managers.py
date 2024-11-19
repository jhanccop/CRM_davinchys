from django.db import models
from datetime import timedelta,datetime
#
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, True, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, True, True, True, **extra_fields)
    
    def usuarios_sistema(self):
        return self.filter(
            is_superuser=False
        ).order_by('-last_login')
    
    def usuarios_sistema_all(self):
        return self.all().order_by('-last_login')
    
    def usuarios_sistema_id(self,id):
        return self.get(
            id=id
        )
    
class DocsManager(models.Manager):
    def docs_por_id(self,id):
        return self.filter(
            idUser__id=id
        )
    def docs_all(self):
        return self.all().order_by('-created')
    def docs_publics(self,intervalo):
        Intervals = intervalo.split(' to ')
        intervals = [ datetime.strptime(dt,"%Y-%m-%d") for dt in Intervals]
        rangeDate = [intervals[0] - timedelta(days = 1),intervals[1] + timedelta(days = 1)]
        return self.filter(
            created__range = rangeDate,
            is_multiple = True
        )