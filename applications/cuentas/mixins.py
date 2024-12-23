from django.shortcuts import redirect, get_object_or_404
from .models import Tin

class VistaConCompaniaMixin:
    def get_compania(self):
        compania_id = self.request.session.get('compania_id')
        if not compania_id:
            return None
        return get_object_or_404(Tin, id=compania_id)