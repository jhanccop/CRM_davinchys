from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import View
#
from .models import User

def check_ocupation_user(position, user_position):
    if (position == User.ADMINISTRADOR or position == user_position or position == User.CEOGLOBAL):
        return True
    else:
        return False
    

def check_ocupation_user2(position, user_position, user_position2):
    #
    
    if (position == User.ADMINISTRADOR or position == User.CEOGLOBAL or position == user_position or position == user_position2):
        
        return True
    else:
        return False

def check_ocupation_user3(position, user_position, user_position2, user_position3):
    if (position == User.ADMINISTRADOR or position == user_position or position == user_position2 or position == user_position3):
        return True
    else:
        return False

def check_ocupation_user4(position, user_position, user_position2, user_position3, user_position4):
    if (position == User.ADMINISTRADOR or position == user_position or position == user_position2 or position == user_position3 or position == user_position4):
        return True
    else:
        return False

class AlmacenPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.PRODUCCION):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)

# =========================== PERMISOS AREA COMERCIAL ===========================
class ComercialMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.COMERCIAL):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:unauthorized'
                )
            )
        return super().dispatch(request, *args, **kwargs)

# =========================== PERMISOS AREA FINANZAS ===========================
class FinanzasMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.FINANZAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:unauthorized'
                )
            )
        return super().dispatch(request, *args, **kwargs)

# =========================== PERMISOS COMERCIAL Y FINANZAS ===========================
class ComercialFinanzasMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user2(request.user.position, User.COMERCIAL, User.FINANZAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:unauthorized'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
# =========================== PERMISOS LOGISTICA Y FINANZAS ===========================
class LogisticaMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.LOGISTICA):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:unauthorized'
                )
            )
        return super().dispatch(request, *args, **kwargs)

# =========================== PERMISOS RRHH ===========================
class RRHHMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.RECURSOSHUMANOS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:unauthorized'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class VentasPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.VENTAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
# =========================== CRM =========================

class TrabajadorPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.COMPRAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class ComprasPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.COMPRAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class ProduccionPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.PRODUCCION):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
class ContabilidadPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.CONTABILIDAD):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'users_app:user-login'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class AdminPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.ADMINISTRADOR):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
class ComprasProducciónPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user2(request.user.position, User.PRODUCCION, User.COMPRAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)
        
class ComprasContabilidadPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user2(request.user.position, User.CONTABILIDAD, User.COMPRAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
class TrabajadorComprasProducciónPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user3(request.user.position, User.PRODUCCION, User.TRABAJADOR, User.COMPRAS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)

class AdminClientsPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user4(request.user.position, User.COMPRAS, User.COMPRAS, User.COMPRAS, User.CONTABILIDAD):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)
    
class RHPermisoMixin(LoginRequiredMixin):
    login_url = reverse_lazy('users_app:user-login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        #
        if not check_ocupation_user(request.user.position, User.RECURSOSHUMANOS):
            # no tiene autorizacion
            return HttpResponseRedirect(
                reverse(
                    'home_app:index'
                )
            )
        return super().dispatch(request, *args, **kwargs)
