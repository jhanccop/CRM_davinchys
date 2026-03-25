from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from applications.RRHH.models import Departamento

# Re-export so other modules can do: from applications.users.mixins import LoginRequiredMixin
__all__ = ['LoginRequiredMixin']


def _has_area_access(user, *areas):
    """
    Returns True if the user's department area is in `areas`,
    or if the user is ADMINISTRADOR or CEOGLOBAL (always allowed).
    """
    try:
        user_area = user.empleado.departamento.idArea
    except AttributeError:
        return False
    if user_area in (Departamento.ADMINISTRADOR, Departamento.CEOGLOBAL):
        return True
    return user_area in areas


class _AreaMixin(LoginRequiredMixin):
    """Base mixin — subclasses set `allowed_areas`."""
    login_url = reverse_lazy('users_app:user-login')
    allowed_areas = ()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not _has_area_access(request.user, *self.allowed_areas):
            return HttpResponseRedirect(reverse('home_app:unauthorized'))
        return super().dispatch(request, *args, **kwargs)


# ── Area mixins ─────────────────────────────────────────────────────────────

class AdministradorMixin(_AreaMixin):
    allowed_areas = (Departamento.ADMINISTRADOR,)

class ComercialMixin(_AreaMixin):
    allowed_areas = (Departamento.COMERCIAL,)

class FinanzasMixin(_AreaMixin):
    allowed_areas = (Departamento.FINANZAS,)

# Alias used by the FINANTIAL module
FinantialMixin = FinanzasMixin

class ProduccionMixin(_AreaMixin):
    allowed_areas = (Departamento.PRODUCCION,)

class GerenciaMixin(_AreaMixin):
    allowed_areas = (Departamento.GERENCIA,)

class LogisticaMixin(_AreaMixin):
    allowed_areas = (Departamento.LOGISTICA,)

class RRHHMixin(_AreaMixin):
    allowed_areas = (Departamento.RECURSOSHUMANOS,)

class TIMixin(_AreaMixin):
    allowed_areas = (Departamento.TI,)


# ── Multi-area mixins ────────────────────────────────────────────────────────

class ComercialFinanzasMixin(_AreaMixin):
    """Comercial o Finanzas (+ Administrador/CEO siempre)."""
    allowed_areas = (Departamento.COMERCIAL, Departamento.FINANZAS)

class ComercialFinanzasLogisticaMixin(_AreaMixin):
    """Comercial, Finanzas o Logística."""
    allowed_areas = (Departamento.COMERCIAL, Departamento.FINANZAS, Departamento.LOGISTICA)

class ProduccionLogisticaMixin(_AreaMixin):
    """Producción o Logística."""
    allowed_areas = (Departamento.PRODUCCION, Departamento.LOGISTICA)

class FinanzasLogisticaMixin(_AreaMixin):
    """Finanzas o Logística (antes: Contabilidad + Compras)."""
    allowed_areas = (Departamento.FINANZAS, Departamento.LOGISTICA)


# ── Legacy names (backward-compatible aliases) ───────────────────────────────
# These names are imported by existing views — keep them pointing to the
# correct area-based mixin so nothing breaks.

# "Almacén" historically mapped to production staff
AlmacenPermisoMixin           = ProduccionMixin

# "Ventas" → Comercial
VentasPermisoMixin            = ComercialMixin

# "Compras" → Logística (purchasing/supply chain)
ComprasPermisoMixin           = LogisticaMixin

# "Producción" → Producción
ProduccionPermisoMixin        = ProduccionMixin

# "Contabilidad" → Finanzas
ContabilidadPermisoMixin      = FinanzasMixin

# "Admin" → Administrador (note: _has_area_access always lets ADMINISTRADOR through,
#  but we still set the area so the mixin rejects non-admin users)
AdminPermisoMixin             = AdministradorMixin

# "Trabajador" (generic worker) → Producción
TrabajadorPermisoMixin        = ProduccionMixin

# "Compras + Producción" → ProduccionLogisticaMixin
ComprasProducciónPermisoMixin              = ProduccionLogisticaMixin
TrabajadorComprasProducciónPermisoMixin    = ProduccionLogisticaMixin

# "Compras + Contabilidad" → FinanzasLogisticaMixin
ComprasContabilidadPermisoMixin = FinanzasLogisticaMixin

# "AdminClients" was used for views accessible by Finanzas, Logística and Comercial.
# The original comment read: "Adquisiciones, Finanzas, Tesorería, contabilidad y administrador"
AdminClientsPermisoMixin = ComercialFinanzasLogisticaMixin

# "RH" → RRHH
RHPermisoMixin = RRHHMixin
