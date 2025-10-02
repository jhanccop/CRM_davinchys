from datetime import date, timedelta
from django.shortcuts import render

from django.views.generic import (
    ListView,
)

from applications.COMERCIAL.purchase.models import requirements

from applications.users.mixins import (
  LogisticaMixin,
  AdminClientsPermisoMixin
)
