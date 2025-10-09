# views.py
from datetime import date, timedelta, datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q, Count, Sum, Avg, When, Value, IntegerField
from django.utils import timezone
import calendar
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.forms import modelformset_factory

from applications.users.mixins import (
    RRHHMixin
)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *

# =========================== Vistas para Empleados ===========================
class EmpleadoListView(RRHHMixin, ListView):
    model = Empleado
    template_name = 'RRHH/empleados/empleados_list.html'
    context_object_name = 'empleados'
    paginate_by = 20

class EmpleadoDetailView(RRHHMixin, DetailView):
    model = Empleado
    template_name = 'RRHH/empleados/empleado_detail.html'

class EmpleadoCreateView(RRHHMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'RRHH/empleados/empleado_form.html'
    permission_required = 'rh.add_empleado'
    success_url = reverse_lazy('rrhh_app:empleados-list')

class EmpleadoUpdateView(RRHHMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'RRHH/empleados/empleado_form.html'
    permission_required = 'rh.change_empleado'
    success_url = reverse_lazy('rrhh_app:empleados-list')

class EmpleadoDeleteView(RRHHMixin, DeleteView):
    model = Empleado
    template_name = 'RRHH/empleados/empleado_confirm_delete.html'
    permission_required = 'rh.delete_empleado'
    success_url = reverse_lazy('rrhh_app:empleados-list')

# =========================== Vistas para Contactos de Emergencia ===========================
class ContactoEmergenciaCreateView(LoginRequiredMixin, CreateView):
    model = ContactoEmergencia
    form_class = ContactoEmergenciaForm
    template_name = 'RRHH/contacto/contacto_form.html'
    
    def get_initial(self):
        empleado = get_object_or_404(Empleado, user=self.request.user)
        return {'empleado': empleado}
    
    def form_valid(self, form):
        form.instance.empleado = self.request.user.empleado
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('empleado-detail', kwargs={'pk': self.request.user.empleado.pk})

class ContactoEmergenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactoEmergencia
    form_class = ContactoEmergenciaForm
    template_name = 'RRHH/contacto/contacto_form.html'
    
    def get_queryset(self):
        return ContactoEmergencia.objects.filter(empleado__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('empleado-detail', kwargs={'pk': self.request.user.empleado.pk})

class ContactoEmergenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactoEmergencia
    template_name = 'RRHH/contacto/contacto_confirm_delete.html'
    
    def get_queryset(self):
        return ContactoEmergencia.objects.filter(empleado__user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('empleado-detail', kwargs={'pk': self.request.user.empleado.pk})

# ====================== Vistas para Asistencia ======================
class AsistenciaCreateView(RRHHMixin, CreateView):
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    template_name = 'RRHH/asistencia/asistencia_form.html'
    success_url = reverse_lazy('rrhh_app:asistencia-list')
    
    #def form_valid(self, form):
    #    form.instance.empleado = self.request.user.empleado
    #    return super().form_valid(form)

class AsistenciaUpdateView(RRHHMixin, UpdateView):
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    template_name = 'RRHH/asistencia/asistencia_form.html'
    success_url = reverse_lazy('rrhh_app:asistencia-list')

class AsistenciaListView(RRHHMixin, ListView):
    model = RegistroAsistencia
    template_name = 'RRHH/asistencia/asistencia_list.html'
    context_object_name = 'registros'
    
    def get_queryset(self):
        queryset = RegistroAsistencia.objects.all()
        
        # Filtro por rango de fechas
        fecha_rango = self.request.GET.get('fecha_rango', '')
        if fecha_rango:
            try:
                fechas = fecha_rango.split(' to ')
                if len(fechas) == 2:
                    fecha_inicio = datetime.strptime(fechas[0], '%Y-%m-%d').date()
                    fecha_fin = datetime.strptime(fechas[1], '%Y-%m-%d').date()
                    queryset = RegistroAsistencia.objects.filtrar_por_fecha(fecha_inicio, fecha_fin)
                elif len(fechas) == 1:
                    fecha = datetime.strptime(fechas[0], '%Y-%m-%d').date()
                    queryset = queryset.filter(fecha=fecha)
            except ValueError:
                # Si hay error en el formato, mostramos los últimos 30 días
                fecha_inicio = timezone.now().date() - timedelta(days=30)
                queryset = queryset.filter(fecha__gte=fecha_inicio)
        else:
            # Por defecto, últimos 30 días
            fecha_inicio = timezone.now().date() - timedelta(days=30)
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        
        # Filtro por empleado
        empleado_id = self.request.GET.get('empleado')
        if empleado_id:
            queryset = queryset.filter(empleado_id=empleado_id)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtro por jornada
        jornada = self.request.GET.get('jornada')
        if jornada:
            queryset = queryset.filter(jornada=jornada)
            
        return queryset.order_by('-fecha', '-hora_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener empleados para el filtro
        from .models import Empleado  # Asegúrate de importar tu modelo Empleado
        context['empleados'] = Empleado.objects.all()
        
        # Pasar los valores actuales de los filtros
        context['fecha_rango_actual'] = self.request.GET.get('fecha_rango', '')
        context['empleado_actual'] = self.request.GET.get('empleado', '')
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['jornada_actual'] = self.request.GET.get('jornada', '')
        
        # Estadísticas
        queryset = self.get_queryset()
        context['total_registros'] = queryset.count()
        context['registros_pendientes'] = queryset.filter(estado=RegistroAsistencia.PENDIENTE).count()
        context['registros_aprobados'] = queryset.filter(estado=RegistroAsistencia.APROBADO).count()
        
        return context

class AsistenciaDeleteView(RRHHMixin, DeleteView):
    model = RegistroAsistencia
    template_name = 'RRHH/asistencia/asistencia_confirm_delete.html'
    #permission_required = 'rh.delete_empleado'
    success_url = reverse_lazy('rrhh_app:asistencia-list')

class RegistroAsistenciaMultipleCreateView(LoginRequiredMixin, CreateView):
    model = RegistroAsistencia
    template_name = 'RRHH/asistencia/registro_multiple.html'
    success_url = reverse_lazy('rrhh_app:asistencia-user-list')
    fields = []
    
    def get_empleado(self):
        """Obtiene el empleado basado en los parámetros de la URL o el usuario"""
        user_id = self.request.user.id
        return Empleado.objects.get(user__id=user_id)
        
    def get_formset_class(self):
        """Retorna la clase del formset (sin instanciar)"""
        return modelformset_factory(
            RegistroAsistencia,
            fields=['fecha', 'hora_inicio', 'hora_final', 'idLocal', 'observaciones'],
            extra=1,
            can_delete=False,  # Añadido para evitar campos DELETE
            widgets={
                'fecha': forms.DateInput(attrs={
                    'type': 'date', 
                    'class': 'form-control fecha-input',
                    'required': 'required'
                }),
                'hora_inicio': forms.TimeInput(attrs={
                    'type': 'time', 
                    'class': 'form-control hora-inicio'
                }),
                'hora_final': forms.TimeInput(attrs={
                    'type': 'time', 
                    'class': 'form-control hora-final'
                }),
                'idLocal': forms.Select(attrs={'class': 'form-control'}),
                'observaciones': forms.Textarea(attrs={
                    'class': 'form-control', 
                    'rows': 2, 
                    'placeholder': 'Observaciones'
                }),
            }
        )

    def get_formset(self, data=None):
        """Retorna una instancia del formset, con data si se proporciona"""
        formset_class = self.get_formset_class()
        if data:
            return formset_class(data, prefix='registros')
        return formset_class(queryset=RegistroAsistencia.objects.none(), prefix='registros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        empleado = self.get_empleado()
        context['empleado'] = empleado
        context['formset'] = self.get_formset()
        
        # Pasar datos para JavaScript
        try:
            from .models import Feriados
            feriados = list(Feriados.objects.values_list('fecha', flat=True))
            context['feriados'] = [f.strftime('%Y-%m-%d') for f in feriados]
        except:
            context['feriados'] = []
        
        return context

    def form_valid(self, form):
        empleado = self.get_empleado()
        if not empleado:
            messages.error(self.request, 'No se pudo identificar al empleado.')
            return self.form_invalid(form)

        # Obtener el formset con los datos POST
        formset = self.get_formset(self.request.POST)
        
        if formset.is_valid():
            registros_guardados = 0
            registros_con_errores = 0
            
            # CAMBIO CLAVE: Usar commit=False para asignar empleado antes de guardar
            instances = formset.save(commit=False)
            
            for i, instance in enumerate(instances):
                # Asignar el empleado ANTES de cualquier validación
                instance.empleado = empleado
                
                try:
                    # Ahora sí validar con el empleado ya asignado
                    instance.full_clean()
                    # Guardar (las jornadas se calcularán automáticamente en save())
                    instance.save()
                    registros_guardados += 1
                    
                except ValidationError as e:
                    registros_con_errores += 1
                    for field, errors in e.error_dict.items():
                        for error in errors:
                            messages.error(
                                self.request, 
                                f"Registro {i+1}: Error en {field} - {error}"
                            )
                except Exception as e:
                    registros_con_errores += 1
                    messages.error(
                        self.request, 
                        f"Registro {i+1}: Error inesperado - {str(e)}"
                    )
            
            # Mostrar resumen
            if registros_guardados > 0:
                messages.success(
                    self.request, 
                    f'Se guardaron {registros_guardados} registros de asistencia correctamente.'
                )
                return HttpResponseRedirect(self.success_url)
            else:
                if registros_con_errores == 0:
                    messages.warning(
                        self.request, 
                        'No se encontraron registros para guardar.'
                    )
                else:
                    messages.error(
                        self.request, 
                        'No se pudo guardar ningún registro. Verifique los datos ingresados.'
                    )
                return self.form_invalid(form)
                
        else:
            # Mostrar errores específicos del formset
            for i, form_in_formset in enumerate(formset):
                if form_in_formset.errors:
                    for field, errors in form_in_formset.errors.items():
                        for error in errors:
                            field_label = form_in_formset.fields[field].label if field in form_in_formset.fields else field
                            messages.error(
                                self.request, 
                                f"Registro {i+1}: Error en {field_label} - {error}"
                            )
            
            # Errores no relacionados con formularios específicos
            if formset.non_form_errors():
                for error in formset.non_form_errors():
                    messages.error(self.request, f"Error general: {error}")
                    
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, corrija los errores en el formulario.')
        return super().form_invalid(form)

# =========================== MY ESPACE ===========================
class RegistroAsistenciaRapidoView(LoginRequiredMixin,CreateView):
    model = RegistroAsistencia
    fields = ['idLocal', 'observaciones']
    template_name = 'rrhh/modal_registro_rapido.html'
    
    def form_valid(self, form):
        empleado = self.request.user.empleado
        hoy = timezone.now().date()
        
        # Verificar si ya existe registro hoy
        if RegistroAsistencia.objects.filter(
            empleado=empleado, 
            fecha=hoy, 
            jornada_diaria='0'
        ).exists():
            messages.warning(self.request, 'Ya tienes un registro de asistencia para hoy')
            return redirect('rrhh_app:bienvenida')
        
        # Auto-completar datos
        registro = form.save(commit=False)
        registro.empleado = empleado
        registro.fecha = hoy
        registro.hora_inicio = timezone.now().replace(hour=9, minute=00, second=0).time()  # Hora actual
        registro.hora_final = timezone.now().replace(hour=18, minute=00, second=0).time()  # 18:00
        registro.jornada_diaria = '0'  # Jornada regular
        registro.estado = '0'  # Pendiente
        
        registro.save()
        messages.success(self.request, 'Asistencia registrada exitosamente')
        return redirect('home_app:bienvenida')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modal_title'] = 'Registro Rápido de Asistencia'
        return context

class RegistroHorasExtraView(LoginRequiredMixin,CreateView):
    model = RegistroAsistencia
    fields = ['hora_inicio', 'hora_final', 'ubicacion', 'observaciones']
    template_name = 'rrhh/modal_horas_extra.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo_extra = self.kwargs.get('tipo_extra')
        context['tipo_extra'] = tipo_extra
        context['modal_title'] = f'Registro Horas Extra {tipo_extra}'
        
        # Sugerir horarios según el tipo de horas extra
        if tipo_extra == '1':
            context['hora_inicio_sugerida'] = '18:01'
            context['hora_final_sugerida'] = '21:59'
        else:  # tipo_extra == '2'
            context['hora_inicio_sugerida'] = '22:00'
            context['hora_final_sugerida'] = '05:59'
            
        return context
    
    def form_valid(self, form):
        empleado = self.request.user.empleado
        tipo_extra = self.kwargs.get('tipo_extra')
        hoy = timezone.now().date()
        
        registro = form.save(commit=False)
        registro.empleado = empleado
        registro.fecha = hoy
        registro.jornada = tipo_extra
        registro.estado = '0'  # Pendiente
        
        registro.save()
        messages.success(self.request, f'Horas Extra {tipo_extra} registradas exitosamente')
        return redirect('home_app:bienvenida')

class AsistenciaUserListView(LoginRequiredMixin, ListView):
    model = RegistroAsistencia
    template_name = 'RRHH/asistencia/asistencia_list_user.html'
    context_object_name = 'registros'

    def get_queryset(self):
        # Filtrar automáticamente por el usuario logueado
        queryset = RegistroAsistencia.objects.filter(empleado__user=self.request.user)
        
        # Filtro por rango de fechas
        fecha_rango = self.request.GET.get('fecha_rango', '')
        if fecha_rango:
            try:
                fechas = fecha_rango.split(' to ')
                if len(fechas) == 2:
                    fecha_inicio = datetime.strptime(fechas[0], '%Y-%m-%d').date()
                    fecha_fin = datetime.strptime(fechas[1], '%Y-%m-%d').date()
                    queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])
                elif len(fechas) == 1:
                    fecha = datetime.strptime(fechas[0], '%Y-%m-%d').date()
                    queryset = queryset.filter(fecha=fecha)
            except ValueError:
                # Si hay error en el formato, mostramos los últimos 30 días
                fecha_inicio = timezone.now().date() - timedelta(days=30)
                queryset = queryset.filter(fecha__gte=fecha_inicio)
        else:
            # Por defecto, últimos 30 días
            fecha_inicio = timezone.now().date() - timedelta(days=30)
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtro por jornada
        jornada = self.request.GET.get('jornada')
        if jornada:
            queryset = queryset.filter(jornada=jornada)
            
        return queryset.order_by('-fecha', '-hora_inicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener solo el empleado del usuario actual para el filtro
        from .models import Empleado
        try:
            empleado_actual = Empleado.objects.get(user=self.request.user)
            context['empleado_actual'] = empleado_actual
            # Si necesitas la lista de empleados para otros propósitos, puedes mantenerla
            # pero probablemente ya no sea necesaria para filtros
            context['empleados'] = Empleado.objects.filter(user=self.request.user)
        except Empleado.DoesNotExist:
            # Manejar el caso donde el usuario no tiene un empleado asociado
            context['empleado_actual'] = None
            context['empleados'] = Empleado.objects.none()
        
        # Pasar los valores actuales de los filtros
        context['fecha_rango_actual'] = self.request.GET.get('fecha_rango', '')
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['jornada_actual'] = self.request.GET.get('jornada', '')
        
        # Estadísticas
        queryset = self.get_queryset()
        context['total_registros'] = queryset.count()
        context['registros_pendientes'] = queryset.filter(estado=RegistroAsistencia.PENDIENTE).count()
        context['registros_aprobados'] = queryset.filter(estado=RegistroAsistencia.APROBADO).count()
        
        return context

class AsistenciaCreateUserView(LoginRequiredMixin, CreateView):
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    template_name = 'RRHH/asistencia/asistencia_user_form.html'
    success_url = reverse_lazy('rrhh_app:asistencia-user-list')

class AsistenciaUpdateUserView(LoginRequiredMixin, UpdateView):
    model = RegistroAsistencia
    form_class = RegistroAsistenciaForm
    template_name = 'RRHH/asistencia/asistencia_user_form.html'
    success_url = reverse_lazy('rrhh_app:asistencia-user-list')

class AsistenciaDeleteUserView(LoginRequiredMixin, DeleteView):
    model = RegistroAsistencia
    template_name = 'RRHH/asistencia/asistencia_confirm_delete.html'
    #permission_required = 'rh.delete_empleado'
    success_url = reverse_lazy('rrhh_app:asistencia-user-list')

# ====================== Vistas para Documentos ======================
class DocumentoCreateView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'RRHH/documentos/documento_form.html'
    success_url = reverse_lazy('rrhh_app:documentos-list')
    
    def form_valid(self, form):
        form.instance.empleado = self.request.user.empleado
        return super().form_valid(form)

class DocumentoUpdate(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'RRHH/documentos/documento_form.html'
    success_url = reverse_lazy('rrhh_app:documentos-list')
    
    def form_valid(self, form):
        form.instance.empleado = self.request.user.empleado
        return super().form_valid(form)

class DocumentoListView(LoginRequiredMixin, ListView):
    template_name = 'RRHH/documentos/documentos_list.html'
    context_object_name = 'documentos'
    
    def get_queryset(self):
        if self.request.user.has_perm('rh.view_all_documentos'):
            return Documento.objects.all()
        return Documento.objects.filter(empleado__user=self.request.user)
    
    def get_queryset(self,**kwargs):
        idCompany = self.request.user.company.id
        TypeKword = self.request.GET.get("TypeKword", '')
        intervalDate = self.request.GET.get("dateKword", '')

        if intervalDate == "Today" or intervalDate =="":
            intervalDate = str(date.today())

        asistencia = Documento.objects.ObtenerDocumentoPorRangoCompaniaTipo(idCompany,intervalDate,TypeKword)
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["lista"] = asistencia

        return payload

class DocumentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Documento
    template_name = 'RRHH/documentos/documento_confirm_delete.html'
    success_url = reverse_lazy('rrhh_app:documentos-list')
    
    def get_queryset(self):
        if self.request.user.has_perm('rh.delete_documento'):
            return Documento.objects.all()
        return Documento.objects.filter(empleado__user=self.request.user)

# ====================== Vistas para mis Documentos ======================
class DocumentoUserListView(LoginRequiredMixin, ListView):
    template_name = 'RRHH/documentos/mis-documentos-list.html'
    context_object_name = 'documentos'
    
    def get_queryset(self,**kwargs):
        idUser = self.request.user.id
        TypeKword = self.request.GET.get("TypeKword", '')

        docs = Documento.objects.ObtenerDocumentoPorUserTipo(idUser,TypeKword)
        payload = {}
        payload["TypeKword"] = TypeKword
        payload["lista"] = docs

        return payload

class DocumentoCreateUserView(LoginRequiredMixin, CreateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'RRHH/documentos/mis-documentos-form.html'
    success_url = reverse_lazy('rrhh_app:mis-documentos')
    
    def form_valid(self, form):
        form.instance.empleado = self.request.user.empleado
        return super().form_valid(form)

class DocumentoUpdateUserView(LoginRequiredMixin, UpdateView):
    model = Documento
    form_class = DocumentoForm
    template_name = 'RRHH/documentos/mis-documentos-form.html'
    success_url = reverse_lazy('rrhh_app:mis-documentos')
    
    def form_valid(self, form):
        form.instance.empleado = self.request.user.empleado
        return super().form_valid(form)

class DocumentoDeleteUserView(LoginRequiredMixin, DeleteView):
    model = Documento
    template_name = 'RRHH/documentos/mis-documentos-delete.html'
    success_url = reverse_lazy('rrhh_app:mis-documentos')
    
    def get_queryset(self):
        if self.request.user.has_perm('rh.delete_documento'):
            return Documento.objects.all()
        return Documento.objects.filter(empleado__user=self.request.user)


# ====================== Vistas para DASHBOARD ======================
class DashboardView(RRHHMixin, TemplateView):
    """Vista principal del dashboard de RRHH"""
    template_name = 'RRHH/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtros
        periodo = self.request.GET.get('periodo', 'mes_actual')
        departamento_id = self.request.GET.get('departamento')
        empleado_id = self.request.GET.get('empleado')
        
        # Determinar fechas según periodo
        fecha_inicio, fecha_fin = self._get_dates_from_period(periodo)
        
        # Aplicar filtros
        empleados_filtrados = Empleado.objects.filter(activo=True)
        if departamento_id:
            empleados_filtrados = empleados_filtrados.filter(departamento_id=departamento_id)
        if empleado_id:
            empleados_filtrados = empleados_filtrados.filter(id=empleado_id)
        
        context.update({
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'periodo_seleccionado': periodo,
            'departamento_seleccionado': departamento_id,
            'empleado_seleccionado': empleado_id,
            'departamentos': Departamento.objects.all(),
            'empleados': Empleado.objects.filter(activo=True),
            **self._get_widgets_data(empleados_filtrados, fecha_inicio, fecha_fin),
            **self._get_tablas_data(empleados_filtrados, fecha_inicio, fecha_fin)
        })
        
        return context
    
    def _get_dates_from_period(self, periodo):
        hoy = timezone.now().date()
        if periodo == 'semana_actual':
            fecha_inicio = hoy - timedelta(days=hoy.weekday())
            fecha_fin = fecha_inicio + timedelta(days=6)
        elif periodo == 'mes_anterior':
            primer_dia_mes_actual = hoy.replace(day=1)
            ultimo_dia_mes_anterior = primer_dia_mes_actual - timedelta(days=1)
            fecha_inicio = ultimo_dia_mes_anterior.replace(day=1)
            fecha_fin = ultimo_dia_mes_anterior
        elif periodo == 'trimestre_actual':
            trimestre_actual = (hoy.month - 1) // 3 + 1
            mes_inicio = (trimestre_actual - 1) * 3 + 1
            fecha_inicio = hoy.replace(month=mes_inicio, day=1)
            mes_fin = trimestre_actual * 3
            ultimo_dia_mes_fin = hoy.replace(month=mes_fin, day=28) + timedelta(days=4)
            fecha_fin = ultimo_dia_mes_fin - timedelta(days=ultimo_dia_mes_fin.day)
        else:  # mes_actual por defecto
            fecha_inicio = hoy.replace(day=1)
            siguiente_mes = hoy.replace(day=28) + timedelta(days=4)
            fecha_fin = siguiente_mes - timedelta(days=siguiente_mes.day)
        
        return fecha_inicio, fecha_fin
    
    def _get_dias_laborables(self, fecha_inicio, fecha_fin):
        """Calcula la cantidad de días laborables (lunes a viernes) excluyendo feriados"""
        # Obtener todos los feriados en el rango
        feriados = Feriados.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values_list('fecha', flat=True)
        feriados_set = set(feriados)
        
        # Calcular días laborables (lunes=0 a viernes=4)
        dias_laborables = 0
        current_date = fecha_inicio
        hoy = timezone.now().date()
        
        while current_date <= fecha_fin:
            # Solo contar días pasados (excluir días futuros)
            if current_date <= hoy:
                # Es día de semana (lunes a viernes) y no es feriado
                if current_date.weekday() < 5 and current_date not in feriados_set:
                    dias_laborables += 1
            current_date += timedelta(days=1)
        
        return dias_laborables
    
    def _get_widgets_data(self, empleados, fecha_inicio, fecha_fin):
        # Métricas principales
        total_empleados = empleados.count()
        
        # Calcular días laborables reales (solo días pasados)
        dias_laborables_totales = self._get_dias_laborables(fecha_inicio, fecha_fin)
        
        # Ausencias (permisos en el período) - CORREGIDO: considerar solo días laborables
        ausencias = Permiso.objects.filter(
            empleado__in=empleados,
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha_inicio,
            estado='1'  # Aprobado
        ).count()
        
        # Horas extra
        horas_extra = RegistroAsistencia.objects.filter(
            empleado__in=empleados,
            fecha__range=[fecha_inicio, fecha_fin],
            jornada__in=['1', '2']  # HE1 y HE2
        ).aggregate(
            total_he1=Sum('horas', filter=Q(jornada='1')),
            total_he2=Sum('horas', filter=Q(jornada='2'))
        )
        
        # Permisos pendientes
        permisos_pendientes = Permiso.objects.filter(
            empleado__in=empleados,
            estado='0'  # Pendiente
        ).count()
        
        return {
            'total_empleados': total_empleados,
            'ausencias_totales': ausencias,
            'dias_laborables_totales': dias_laborables_totales,  # Nuevo: para referencia
            'horas_extra1': horas_extra['total_he1'] or 0,
            'horas_extra2': horas_extra['total_he2'] or 0,
            'total_departamentos': Departamento.objects.count(),
            'permisos_pendientes': permisos_pendientes
        }
    
    def _get_tablas_data(self, empleados, fecha_inicio, fecha_fin):
        # Tabla de asistencias
        asistencias_data = []
        
        # Obtener feriados una sola vez para optimización
        feriados = Feriados.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values_list('fecha', flat=True)
        feriados_set = set(feriados)
        
        hoy = timezone.now().date()
        
        for empleado in empleados:
            registros = RegistroAsistencia.objects.filter(
                empleado=empleado,
                fecha__range=[fecha_inicio, fecha_fin]
            )
            
            # CORRECCIÓN: Contar días asistidos únicos
            dias_asistidos = registros.values('fecha').distinct().count()
            
            # CORRECCIÓN: Calcular días laborables reales para este empleado
            dias_laborables_empleado = 0
            current_date = fecha_inicio
            
            while current_date <= fecha_fin:
                # Solo contar días pasados (excluir días futuros)
                if current_date <= hoy:
                    # Es día de semana (lunes a viernes) y no es feriado
                    if current_date.weekday() < 5 and current_date not in feriados_set:
                        dias_laborables_empleado += 1
                current_date += timedelta(days=1)
            
            # Calcular ausencias basadas en días laborables reales
            ausencias_empleado = max(0, dias_laborables_empleado - dias_asistidos)
            porcentaje_asistencia = (dias_asistidos / dias_laborables_empleado * 100) if dias_laborables_empleado > 0 else 0
            
            # Horas extra
            horas_extra1 = registros.filter(jornada='1').aggregate(
                total=Sum('horas')
            )['total'] or 0
            
            horas_extra2 = registros.filter(jornada='2').aggregate(
                total=Sum('horas')
            )['total'] or 0
            
            asistencias_data.append({
                'empleado': empleado,
                'departamento': empleado.departamento,
                'dias_asistidos': dias_asistidos,
                'dias_laborables': dias_laborables_empleado,  # Nuevo: para referencia
                'ausencias': ausencias_empleado,
                'porcentaje_asistencia': round(porcentaje_asistencia, 1),
                'horas_extra1': round(float(horas_extra1), 1),
                'horas_extra2': round(float(horas_extra2), 1)
            })
        
        # Tabla de documentación
        documentacion_data = []
        for empleado in empleados:
            documentos_existen = Documento.objects.documentos_completos_empleado(empleado.id)
            porcentaje_completado = Documento.objects.porcentaje_completado(empleado.id)
            
            documentacion_data.append({
                'empleado': empleado,
                'departamento': empleado.departamento,
                'cv': documentos_existen.get('2', False),
                'contrato': documentos_existen.get('1', False),
                'certificados': documentos_existen.get('4', False),
                'boleta': documentos_existen.get('0', False),
                'porcentaje_completado': round(porcentaje_completado, 1)
            })
        
        # Tabla de permisos solicitados
        permisos_data = Permiso.objects.filter(
            empleado__in=empleados
        ).select_related('empleado', 'empleado__departamento').order_by('-created')[:10]
        
        # Tabla de departamentos
        departamentos_data = []
        for departamento in Departamento.objects.all():
            empleados_depto = empleados.filter(departamento=departamento)
            if not empleados_depto.exists():
                continue
                
            metricas_depto = self._get_metricas_departamento(empleados_depto, fecha_inicio, fecha_fin)
            departamentos_data.append({
                'departamento': departamento,
                'numero_empleados': empleados_depto.count(),
                **metricas_depto
            })
        
        return {
            'asistencias_data': asistencias_data,
            'documentacion_data': documentacion_data,
            'permisos_data': permisos_data,
            'departamentos_data': departamentos_data
        }
    
    def _get_metricas_departamento(self, empleados, fecha_inicio, fecha_fin):
        # Obtener feriados
        feriados = Feriados.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values_list('fecha', flat=True)
        feriados_set = set(feriados)
        
        hoy = timezone.now().date()
        
        # Calcular días laborables totales para el departamento
        dias_laborables_totales = 0
        current_date = fecha_inicio
        while current_date <= fecha_fin:
            if current_date <= hoy and current_date.weekday() < 5 and current_date not in feriados_set:
                dias_laborables_totales += 1
            current_date += timedelta(days=1)
        
        # Calcular promedio de asistencia
        total_porcentajes = 0
        horas_extra1_total = 0
        horas_extra2_total = 0
        
        for empleado in empleados:
            registros = RegistroAsistencia.objects.filter(
                empleado=empleado,
                fecha__range=[fecha_inicio, fecha_fin]
            )
            
            dias_asistidos = registros.values('fecha').distinct().count()
            porcentaje = (dias_asistidos / dias_laborables_totales * 100) if dias_laborables_totales > 0 else 0
            total_porcentajes += porcentaje
            
            # Sumar horas extra
            he1 = registros.filter(jornada='1').aggregate(total=Sum('horas'))['total'] or 0
            he2 = registros.filter(jornada='2').aggregate(total=Sum('horas'))['total'] or 0
            
            horas_extra1_total += float(he1)
            horas_extra2_total += float(he2)
        
        promedio_asistencia = total_porcentajes / empleados.count() if empleados.count() > 0 else 0
        
        return {
            'promedio_asistencia': round(promedio_asistencia, 1),
            'horas_extra1_totales': round(horas_extra1_total, 1),
            'horas_extra2_totales': round(horas_extra2_total, 1),
            'dias_laborables_totales': dias_laborables_totales  # Nuevo: para referencia
        }

class ReporteAsistenciaPersonaView(RRHHMixin, TemplateView):
    template_name = 'RRHH/reporte_asistencia_persona.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener parámetros de filtro
        empleado_id = self.request.GET.get('empleado')
        fecha_inicio_str = self.request.GET.get('fecha_inicio')
        fecha_fin_str = self.request.GET.get('fecha_fin')
        
        # Establecer fechas por defecto (mes actual)
        hoy = timezone.now().date()
        if not fecha_inicio_str:
            fecha_inicio = hoy.replace(day=1)
        else:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            
        if not fecha_fin_str:
            siguiente_mes = hoy.replace(day=28) + timedelta(days=4)
            fecha_fin = siguiente_mes - timedelta(days=siguiente_mes.day)
        else:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        
        # Obtener empleado específico o todos los activos
        if empleado_id:
            empleados = Empleado.objects.filter(id=empleado_id, activo=True)
        else:
            empleados = Empleado.objects.filter(activo=True)
        
        # Obtener feriados para todo el período (optimización)
        feriados = Feriados.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).values_list('fecha', flat=True)
        feriados_set = set(feriados)
        
        reportes = []
        for empleado in empleados:
            reporte = self._generar_reporte_empleado(empleado, fecha_inicio, fecha_fin, feriados_set)
            reportes.append(reporte)
        
        # Calcular días laborables totales para el período
        dias_laborables_totales = self._calcular_dias_laborables(fecha_inicio, fecha_fin, feriados_set)
        
        context.update({
            'reportes': reportes,
            'empleados': Empleado.objects.filter(activo=True),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'empleado_seleccionado': empleado_id,
            'total_dias_periodo': (fecha_fin - fecha_inicio).days + 1,
            'dias_laborables_totales': dias_laborables_totales,
        })
        
        return context
    
    def _calcular_dias_laborables(self, fecha_inicio, fecha_fin, feriados_set):
        """Calcula la cantidad de días laborables (lunes a viernes) excluyendo feriados y días futuros"""
        hoy = timezone.now().date()
        dias_laborables = 0
        current_date = fecha_inicio
        
        while current_date <= fecha_fin:
            # Solo contar días pasados (excluir días futuros)
            if current_date <= hoy:
                # Es día de semana (lunes a viernes) y no es feriado
                if current_date.weekday() < 5 and current_date not in feriados_set:
                    dias_laborables += 1
            current_date += timedelta(days=1)
        
        return dias_laborables
    
    def _generar_reporte_empleado(self, empleado, fecha_inicio, fecha_fin, feriados_set):
        """Generar reporte completo para un empleado"""
        
        # 1. Obtener todos los registros de asistencia en el período
        registros = RegistroAsistencia.objects.filter(
            empleado=empleado,
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by('fecha', 'hora_inicio')
        
        # 2. Calcular días laborables para este empleado
        dias_laborables = self._calcular_dias_laborables(fecha_inicio, fecha_fin, feriados_set)
        
        # 3. Calcular métricas básicas
        metricas = self._calcular_metricas_basicas(registros, fecha_inicio, fecha_fin, empleado, dias_laborables, feriados_set)
        
        # 4. Calcular horas trabajadas por día
        horas_por_dia = self._calcular_horas_por_dia(registros, feriados_set)
        
        # 5. Obtener permisos en el período
        permisos = self._obtener_permisos_empleado(empleado, fecha_inicio, fecha_fin)
        
        # 6. Generar resumen por semanas
        resumen_semanas = self._generar_resumen_semanas(horas_por_dia, fecha_inicio, fecha_fin, feriados_set)
        
        return {
            'empleado': empleado,
            'metricas': metricas,
            'horas_por_dia': horas_por_dia,
            'permisos': permisos,
            'resumen_semanas': resumen_semanas,
            'registros_detallados': list(registros),  # Para mostrar en tabla detallada
            'dias_laborables': dias_laborables,
        }
    
    def _calcular_metricas_basicas(self, registros, fecha_inicio, fecha_fin, empleado, dias_laborables, feriados_set):
        """Calcular todas las métricas del reporte considerando solo días laborables"""
        
        # Días con registros de asistencia (días trabajados)
        dias_trabajados = registros.values('fecha').distinct().count()
        
        # CORRECCIÓN: Horas trabajadas sumando el campo 'horas' calculado del modelo
        horas_totales = registros.aggregate(
            total_horas=Sum('horas')
        )['total_horas'] or 0
        
        # Horas por tipo de jornada
        horas_por_jornada = registros.aggregate(
            horas_regulares=Sum('horas', filter=Q(jornada=RegistroAsistencia.REGULAR)),
            horas_he1=Sum('horas', filter=Q(jornada=RegistroAsistencia.HEXTRA1)),
            horas_he2=Sum('horas', filter=Q(jornada=RegistroAsistencia.HEXTRA2)),
            horas_feriados=Sum('horas', filter=Q(jornada=RegistroAsistencia.FERIADO))
        )
        
        horas_regulares = horas_por_jornada['horas_regulares'] or 0
        horas_he1 = horas_por_jornada['horas_he1'] or 0
        horas_he2 = horas_por_jornada['horas_he2'] or 0
        horas_feriados = horas_por_jornada['horas_feriados'] or 0
        
        # Días feriados laborados
        dias_feriados_laborados = registros.filter(
            jornada=RegistroAsistencia.FERIADO
        ).values('fecha').distinct().count()
        
        # Días regulares laborados (excluyendo feriados)
        dias_regulares_laborados = registros.filter(
            jornada=RegistroAsistencia.REGULAR
        ).values('fecha').distinct().count()
        
        # Permisos
        permisos = Permiso.objects.filter(
            empleado=empleado,
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha_inicio
        )
        
        permisos_solicitados = permisos.count()
        permisos_aprobados = permisos.filter(estado='1').count()
        permisos_pendientes = permisos.filter(estado='0').count()
        
        # Horas de permisos aprobados
        horas_permisos_aprobados = permisos.filter(estado='1').aggregate(
            total=Sum('horas')
        )['total'] or 0
        
        # CORRECCIÓN: Inasistencias basadas en días laborables
        dias_inasistencia = max(0, dias_laborables - dias_regulares_laborados)
        
        # Horas esperadas (8 horas por día laborable)
        horas_esperadas = dias_laborables * 8
        
        # Horas inasistencia (solo días laborables que no se trabajaron)
        horas_inasistencia = dias_inasistencia * 8
        
        # CORRECCIÓN: Porcentajes basados en días laborables
        porcentaje_asistencia = (dias_regulares_laborados / dias_laborables * 100) if dias_laborables > 0 else 0
        
        # Eficiencia basada en horas trabajadas vs horas esperadas en días laborables
        porcentaje_eficiencia = (horas_totales / horas_esperadas * 100) if horas_esperadas > 0 else 0
        
        # Ubicaciones de trabajo
        ubicaciones = registros.values('ubicacion').annotate(
            total_dias=Count('fecha', distinct=True),
            total_horas=Sum('horas')
        )
        
        return {
            'total_dias_periodo': (fecha_fin - fecha_inicio).days + 1,
            'dias_laborables': dias_laborables,
            'dias_trabajados': dias_trabajados,
            'dias_regulares_laborados': dias_regulares_laborados,
            'dias_inasistencia': dias_inasistencia,
            'horas_totales': round(float(horas_totales), 2),
            'horas_regulares': round(float(horas_regulares), 2),
            'horas_extra1': round(float(horas_he1), 2),
            'horas_extra2': round(float(horas_he2), 2),
            'horas_feriados': round(float(horas_feriados), 2),
            'dias_feriados_laborados': dias_feriados_laborados,
            'permisos_solicitados': permisos_solicitados,
            'permisos_aprobados': permisos_aprobados,
            'permisos_pendientes': permisos_pendientes,
            'horas_permisos_aprobados': float(horas_permisos_aprobados),
            'horas_inasistencia': horas_inasistencia,
            'horas_esperadas': horas_esperadas,
            'porcentaje_asistencia': round(porcentaje_asistencia, 1),
            'porcentaje_eficiencia': round(porcentaje_eficiencia, 1),
            'ubicaciones': list(ubicaciones),
        }
    
    def _calcular_horas_por_dia(self, registros, feriados_set):
        """Calcular horas trabajadas por día, considerando el nuevo modelo"""
        horas_por_dia = {}
        
        # Agrupar registros por fecha
        fechas = registros.values_list('fecha', flat=True).distinct()
        
        for fecha in fechas:
            registros_dia = registros.filter(fecha=fecha).order_by('hora_inicio')
            
            # Determinar tipo de día
            es_laborable = fecha.weekday() < 5  # Lunes a viernes
            es_feriado = fecha in feriados_set
            es_futuro = fecha > timezone.now().date()
            
            # Sumar horas totales del día
            horas_dia = registros_dia.aggregate(total=Sum('horas'))['total'] or 0
            
            # Horas por tipo de jornada
            horas_jornada = registros_dia.aggregate(
                regular=Sum('horas', filter=Q(jornada=RegistroAsistencia.REGULAR)),
                he1=Sum('horas', filter=Q(jornada=RegistroAsistencia.HEXTRA1)),
                he2=Sum('horas', filter=Q(jornada=RegistroAsistencia.HEXTRA2)),
                feriado=Sum('horas', filter=Q(jornada=RegistroAsistencia.FERIADO))
            )
            
            # Primer y último registro del día
            primer_registro = registros_dia.first()
            ultimo_registro = registros_dia.last()
            
            # Ubicaciones utilizadas en el día
            ubicaciones = registros_dia.values('ubicacion').annotate(
                count=Count('id')
            )
            
            horas_por_dia[fecha] = {
                'fecha': fecha,
                'primer_registro': primer_registro.hora_inicio if primer_registro else None,
                'ultimo_registro': ultimo_registro.hora_final if ultimo_registro else None,
                'total_registros': registros_dia.count(),
                'horas_totales': round(float(horas_dia), 2),
                'horas_regulares': round(float(horas_jornada['regular'] or 0), 2),
                'horas_extra1': round(float(horas_jornada['he1'] or 0), 2),
                'horas_extra2': round(float(horas_jornada['he2'] or 0), 2),
                'horas_feriado': round(float(horas_jornada['feriado'] or 0), 2),
                'es_feriado': es_feriado,
                'es_laborable': es_laborable,
                'es_futuro': es_futuro,
                'ubicaciones': list(ubicaciones),
                'registros': list(registros_dia)
            }
        
        return horas_por_dia
    
    def _obtener_permisos_empleado(self, empleado, fecha_inicio, fecha_fin):
        """Obtener permisos del empleado en el período"""
        permisos = Permiso.objects.filter(
            empleado=empleado,
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha_inicio
        ).order_by('-fecha_inicio')
        
        return [
            {
                'tipo': permiso.get_tipo_display(),
                'fecha_inicio': permiso.fecha_inicio,
                'fecha_fin': permiso.fecha_fin,
                'horas': permiso.horas,
                'estado': permiso.get_estado_display(),
                'estado_codigo': permiso.estado,
                'dias': (permiso.fecha_fin - permiso.fecha_inicio).days + 1
            }
            for permiso in permisos
        ]
    
    def _generar_resumen_semanas(self, horas_por_dia, fecha_inicio, fecha_fin, feriados_set):
        """Generar resumen semanal considerando solo días laborables"""
        resumen_semanas = {}
        
        fecha_actual = fecha_inicio
        hoy = timezone.now().date()
        
        while fecha_actual <= fecha_fin:
            # Obtener número de semana
            semana_num = fecha_actual.isocalendar()[1]
            año = fecha_actual.year
            
            clave_semana = f"{año}-W{semana_num}"
            
            if clave_semana not in resumen_semanas:
                # Calcular días laborables para esta semana
                dias_laborables_semana = 0
                fecha_temp = fecha_actual
                while fecha_temp <= min(fecha_actual + timedelta(days=6), fecha_fin):
                    if fecha_temp <= hoy and fecha_temp.weekday() < 5 and fecha_temp not in feriados_set:
                        dias_laborables_semana += 1
                    fecha_temp += timedelta(days=1)
                
                resumen_semanas[clave_semana] = {
                    'semana_num': semana_num,
                    'año': año,
                    'fecha_inicio': fecha_actual,
                    'fecha_fin': min(fecha_actual + timedelta(days=6), fecha_fin),
                    'dias_trabajados': 0,
                    'dias_laborables': dias_laborables_semana,
                    'horas_totales': 0,
                    'horas_regulares': 0,
                    'horas_extra1': 0,
                    'horas_extra2': 0,
                    'horas_feriado': 0,
                    'dias_feriados_laborados': 0
                }
            
            # Acumular datos del día si existe en el reporte
            if fecha_actual in horas_por_dia:
                dia_data = horas_por_dia[fecha_actual]
                resumen_semanas[clave_semana]['dias_trabajados'] += 1
                resumen_semanas[clave_semana]['horas_totales'] += dia_data['horas_totales']
                resumen_semanas[clave_semana]['horas_regulares'] += dia_data['horas_regulares']
                resumen_semanas[clave_semana]['horas_extra1'] += dia_data['horas_extra1']
                resumen_semanas[clave_semana]['horas_extra2'] += dia_data['horas_extra2']
                resumen_semanas[clave_semana]['horas_feriado'] += dia_data['horas_feriado']
                
                if dia_data['es_feriado']:
                    resumen_semanas[clave_semana]['dias_feriados_laborados'] += 1
            
            fecha_actual += timedelta(days=1)
        
        # Calcular porcentajes y métricas adicionales para cada semana
        for semana in resumen_semanas.values():
            # Porcentaje de asistencia
            if semana['dias_laborables'] > 0:
                semana['porcentaje_asistencia'] = round(
                    (semana['dias_trabajados'] / semana['dias_laborables'] * 100), 1
                )
            else:
                semana['porcentaje_asistencia'] = 0
            
            # Horas esperadas (8 horas por día laborable)
            semana['horas_esperadas'] = semana['dias_laborables'] * 8
            
            # Porcentaje de eficiencia
            if semana['horas_esperadas'] > 0:
                semana['porcentaje_eficiencia'] = round(
                    (semana['horas_totales'] / semana['horas_esperadas'] * 100), 1
                )
            else:
                semana['porcentaje_eficiencia'] = 0
        
        return list(resumen_semanas.values())
    
