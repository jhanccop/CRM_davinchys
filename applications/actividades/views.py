from datetime import date, timedelta, datetime
from django.utils import timezone
import json
from decimal import Decimal
import datetime

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db import transaction

from django.urls import reverse_lazy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    View,
    TemplateView
)

from applications.users.mixins import AdminPermisoMixin,ProduccionPermisoMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (
  TrafoQuote,
  Trafos,
  Projects,
  Commissions,
  DailyTasks,
  RestDays,
  EmailSent,
  TrafoTask,
  SuggestionBox
)
from applications.users.models import User
from applications.cuentas.models import Tin

from .forms import (
  TrafoForm,
  QuoteTrafoForm,
  ProjectsForm,
  CommissionsForm,
  DailyTaskForm,
  RestDaysForm,
  EmailSentForm,
  TrafoTaskForm,
  SuggestionBoxForm
)
# ======================= PROYECTOS ===========================
class ProjectsListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-proyectos.html"
    context_object_name = 'proyecto'
    model = Projects

class ProjectsCreateView(AdminPermisoMixin, CreateView):
    template_name = "actividades/crear-proyecto.html"
    model = Projects
    form_class = ProjectsForm
    success_url = reverse_lazy('activities_app:proyecto-lista')

class ProjectsDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-proyecto.html"
    model = Projects
    success_url = reverse_lazy('activities_app:proyecto-lista')

class ProjectsUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "actividades/editar-proyecto.html"
    model = Projects
    form_class = ProjectsForm
    success_url = reverse_lazy('activities_app:proyecto-lista')

# ======================= COMISIONES ===========================
class CommissionsListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-comision.html"
    context_object_name = 'comision'
    model = Commissions

class CommissionsCreateView(AdminPermisoMixin,CreateView):
    template_name = "actividades/crear-comision.html"
    model = Commissions
    form_class = CommissionsForm
    success_url = reverse_lazy('activities_app:comision-lista')

class CommissionsDeleteView(AdminPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-comision.html"
    model = Commissions
    success_url = reverse_lazy('activities_app:comision-lista')

class CommissionsUpdateView(AdminPermisoMixin,UpdateView):
    template_name = "actividades/editar-comision.html"
    model = Commissions
    form_class = CommissionsForm
    success_url = reverse_lazy('activities_app:comision-lista')

        
# ======================== TAREAS DIARIAS CALENDARIO =======================

class DailyTaskReportView(AdminPermisoMixin,ListView):
    template_name = "actividades/reporte-actividades-diarias.html"
    context_object_name = 'actividadesDiarias'
    model = DailyTasks

    def get_queryset(self):
        userid = self.request.GET.get("UserKword", '')
        selected = self.request.GET.get("TypeKword", '')
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 7)) + " to " + str(date.today())
        
        if selected =="" or selected == None:
            selected = "2" # todo
        
        if userid =="" or userid == None:
            userid=self.request.user.id

        payload = {}
        payload["selected"] = selected
        payload["user_selected"] = User.objects.usuarios_sistema_id(id=int(userid))
        payload["users"] = User.objects.usuarios_sistema_all()
        payload["intervalDate"] = intervalDate

        # View admin or no
       
        if selected == "1":
            payload["actividades"]= DailyTasks.objects.MiListarPorIntervaloHorasExtra(user=int(userid),interval=intervalDate)
        else:
            payload["actividades"] = DailyTasks.objects.MiListarPorIntervalo(user=int(userid),interval=intervalDate,type=selected)
        payload["dias"] = DailyTasks.objects.MiListarPorIntervaloDias(user=int(userid),interval=intervalDate)
        payload["acc"] = DailyTasks.objects.MiListarPorIntervaloHorasExtraAcc(user=int(userid),interval=intervalDate)
        return payload
    
# ======================== ACTIVIDADES POR SEMANA =======================
#class MyWeeklyTaskListView(AdminPermisoMixin,ListView):
#    template_name = "actividades/mi-lista-actividades-semanales.html"
#    context_object_name = 'actividadesDiarias'
#    model = DailyTasks


class WeeklyTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'actividades/mi-lista-actividades-semanales.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dateSelected = self.request.GET.get("week", '')

        if dateSelected == "" or dateSelected == "current":
            today = timezone.now().date()
            year = today.year
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            week = today.isocalendar()[1]
            
            # Generar días de la semana
            week_days = [start_of_week + timedelta(days=i) for i in range(7)]
            
            # Obtener tareas del usuario para la semana actual
            tasks = DailyTasks.objects.filter(
                user=self.request.user,
                date__range=[start_of_week, end_of_week]
            ).order_by('date')

        else:
            year, week = int(dateSelected.split(" - ")[0]) , int(dateSelected.split(" - ")[1])

            referencia = datetime.date(year, 1, 4)
            año_iso, semana_iso, dia_semana = referencia.isocalendar()
            lunes_semana_1 = referencia - datetime.timedelta(days=dia_semana - 1)
            start_of_week = lunes_semana_1 + datetime.timedelta(weeks = week - 1)
            end_of_week = start_of_week + datetime.timedelta(days=6)

        currentWeek = timezone.now().date().isocalendar()[1]
        # Generar días de la semana
        week_days = [start_of_week + timedelta(days=i) for i in range(7)]
        
        # Obtener tareas del usuario para la semana actual
        tasks = DailyTasks.objects.filter(
            user=self.request.user,
            date__range=[start_of_week, end_of_week]
        ).order_by('date')
        
        tasks_by_day = {}
        daily_totals = {}  # Nuevo diccionario para los totales
        
        for day in week_days:
            day_tasks = [t for t in tasks if t.date == day]
            tasks_by_day[day] = day_tasks
            
            # Calcular totales para el día
            total_reg = sum(t.hours or 0 for t in day_tasks)
            total_overtime = sum(t.overTime or 0 for t in day_tasks)
            daily_totals[day] = {
                'hours': total_reg,
                'overtime': total_overtime,
                'total': total_reg + total_overtime
            }

        # Calcular totales
        total_reg = sum(task.hours or 0 for task in tasks)
        total_activities = tasks.count()
        overtime = sum(task.overTime or 0 for task in tasks)
        
        # Obtener historial de semanas anteriores
        history = self.get_weekly_history(self.request.user)

        # obtener compañias
        companies = Tin.objects.all()
        rest_days = RestDays.objects.getRestTimesNoCompensateById(self.request.user.id)
        
        context.update({
            'weekList':[f"{year} - {i}" for i in range(1,currentWeek + 1)  ],
            "weekSelected" : f"{year} - {week}",
            'week_days': week_days,
            'tasks_by_day': tasks_by_day,
            'daily_totals': daily_totals,
            'week_number': week,
            'start_of_week': start_of_week,
            'end_of_week': end_of_week,
            'total_reg': total_reg,
            'total_hours': total_reg + overtime,
            'total_activities': total_activities,
            'overtime': overtime,
            'history': history,
            'model': DailyTasks,
            'companies': companies,
            'type_choices' : DailyTasks.TYPE_CHOICES,
            'work_choices' : DailyTasks.WORK_CHOICES,
            'rest_days' : rest_days
        })
        return context
    
    def get_weekly_history(self, user, weeks=3):
        today = timezone.now().date()
        history = []
        
        for i in range(1, weeks + 1):
            start_date = today - timedelta(weeks=i)
            start_date = start_date - timedelta(days=start_date.weekday())
            end_date = start_date + timedelta(days=6)
            
            tasks = DailyTasks.objects.filter(
                user=user,
                date__range=[start_date, end_date]
            )
            
            total_hours = sum(task.hours or 0 for task in tasks)
            total_activities = tasks.count()
            
            history.append({
                'week_number': start_date.isocalendar()[1],
                'start_date': start_date,
                'end_date': end_date,
                'total_hours': total_hours,
                'total_activities': total_activities,
            })
        
        return history

class CreateDailyTaskView(LoginRequiredMixin, CreateView):
    model = DailyTasks
    fields = ['date', 'activity', 'type', 'hours', 'overTime', 'idTin', 'rest_day', 'task',
              'trafoOrder', 'commissions', 'projects', 'assignedTasks']
    #template_name = 'actividades/create_task.html'
    success_url = reverse_lazy('activities_app:weekly_tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class UpdateDailyTaskView(LoginRequiredMixin, UpdateView):
    model = DailyTasks
    fields = ['date', "task",'activity', 'type', 'hours', 'overTime', 'idTin', 'rest_day']
    template_name = 'actividades/edit_task.html'
    success_url = reverse_lazy('activities_app:weekly_tasks')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Agregar clases CSS a cada campo
        form.fields['date'].widget.attrs.update({'class': 'form-control'})
        form.fields['activity'].widget.attrs.update({'class': 'form-control','rows':2})
        form.fields['type'].widget.attrs.update({'class': 'form-control'})  # Para selects
        form.fields['task'].widget.attrs.update({'class': 'form-control'})  # Para selects
        form.fields['hours'].widget.attrs.update({'class': 'form-control'})
        form.fields['overTime'].widget.attrs.update({'class': 'form-control'})
        form.fields['idTin'].widget.attrs.update({'class': 'form-control'})
        form.fields['rest_day'].widget.attrs.update({'class': 'form-control'})
        
        # También puedes agregar otros atributos
        form.fields['date'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Selecciona una fecha'
        })
        
        return form
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Tin.objects.all()
        context['type_choices'] = DailyTasks.TYPE_CHOICES
        context['work_choices'] = DailyTasks.WORK_CHOICES
        return context
    
    def get(self, request, *args, **kwargs):
        """Manejar peticiones GET para cargar el formulario via AJAX"""
        self.object = self.get_object()
        context = self.get_context_data()
        
        # Si es una petición AJAX, devolver solo el formulario
        if request.headers.get('Accept') == 'text/html' and not request.headers.get('X-Requested-With'):
            # Petición normal del navegador
            return super().get(request, *args, **kwargs)
        else:
            # Petición AJAX o fetch - devolver solo el contenido del formulario
            return render(request, 'actividades/edit_task_form.html', context)
    
    def form_valid(self, form):
        """Manejar el envío exitoso del formulario"""
        response = super().form_valid(form)
        
        # Si es una petición AJAX, devolver JSON
        if self.request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Actividad actualizada correctamente'})
        
        return response
    
    def form_invalid(self, form):
        """Manejar errores de validación"""
        if self.request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'success': False, 
                'errors': form.errors,
                'message': 'Error al actualizar la actividad'
            }, status=400)
        
        return super().form_invalid(form)

class DeleteDailyTaskView(LoginRequiredMixin, DeleteView):
    model = DailyTasks
    template_name = 'actividades/delete_task.html'
    success_url = reverse_lazy('activities_app:weekly_tasks')
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Sobrescribe el método delete para manejar AJAX"""
        self.object = self.get_object()
        
        try:
            self.object.delete()
            
            # Si es una petición AJAX, devolver JSON
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'success': True, 'message': 'Actividad eliminada correctamente'})
            
            # Petición normal - redirigir
            return super().delete(request, *args, **kwargs)
            
        except Exception as e:
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'message': f'Error al eliminar la actividad: {str(e)}'
                }, status=500)
            
            # En caso de error en petición normal, redirigir con mensaje
            return super().delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Sobrescribe el método post para asegurar el manejo correcto"""
        return self.delete(request, *args, **kwargs)
# ======================= DESCANSOS ===========================

class MyListRestDays(LoginRequiredMixin,ListView):
    model = RestDays
    template_name = "actividades/mi-lista-permisos.html"
    context_object_name = 'permisos'

class RestTimeCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/crear-permiso-laboral.html"
    model = RestDays
    form_class = RestDaysForm
    success_url = reverse_lazy('activities_app:mi-lista-permisos')

class RestTimeDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "actividades/eliminar-permiso-laboral.html"
    model = RestDays
    success_url = reverse_lazy('activities_app:mi-lista-permisos')

class RestTimeUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "actividades/editar-permiso-laboral.html"
    model = RestDays
    form_class = RestDaysForm
    success_url = reverse_lazy('activities_app:mi-lista-permisos')

# ===== MODALS ====


@method_decorator(csrf_exempt, name='dispatch')
class AprobarPermisoRRHHView(LoginRequiredMixin, View):
    """Vista para aprobación de permisos por RRHH"""
    
    def post(self, request, *args, **kwargs):
        permiso_id = request.POST.get('permiso_id')
        comentario = request.POST.get('comentario', '')
        
        try:
            permiso = RestDays.objects.get(id=permiso_id)
            
            # Verificar que el usuario sea de RRHH (position == "9")
            if request.user.position != "9":
                return JsonResponse({
                    'status': 'error',
                    'message': 'No tienes permisos para esta acción'
                }, status=403)
            
            # Aprobar en nivel RRHH
            permiso.tag1 = RestDays.ACEPTADO
            permiso.dt1 = timezone.now()
            
            if comentario:
                permiso.motive = f"{permiso.motive}\nAprobado por RRHH: {comentario}"
            
            permiso.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Permiso aprobado por RRHH'
            })
            
        except RestDays.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Permiso no encontrado'
            }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class DenegarPermisoRRHHView(LoginRequiredMixin, View):
    """Vista para denegación de permisos por RRHH"""
    
    def post(self, request, *args, **kwargs):
        permiso_id = request.POST.get('permiso_id')
        comentario = request.POST.get('comentario', '')
        
        if not comentario:
            return JsonResponse({
                'status': 'error',
                'message': 'Debe ingresar un motivo de denegación'
            }, status=400)
        
        try:
            permiso = RestDays.objects.get(id=permiso_id)
            
            if request.user.position != "9":
                return JsonResponse({
                    'status': 'error',
                    'message': 'No tienes permisos para esta acción'
                }, status=403)
            
            # Denegar en nivel RRHH
            permiso.tag1 = RestDays.DENEGADO
            permiso.dt1 = timezone.now()
            permiso.motive = permiso.motive + "\n" + f"Denegado por RRHH: {comentario}"
            permiso.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Permiso denegado por RRHH'
            })
            
        except RestDays.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Permiso no encontrado'
            }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class AprobarPermisoGerenciaView(LoginRequiredMixin, View):
    """Vista para aprobación de permisos por Gerencia"""
    
    def post(self, request, *args, **kwargs):
        permiso_id = request.POST.get('permiso_id')
        comentario = request.POST.get('comentario', '')
        
        try:
            permiso = RestDays.objects.get(id=permiso_id)
            
            # Verificar que el usuario sea de Gerencia (position == "0")
            if request.user.position != "0":
                return JsonResponse({
                    'status': 'error',
                    'message': 'No tienes permisos para esta acción'
                }, status=403)
            
            # Verificar que esté aprobado por RRHH primero
            if permiso.tag1 != RestDays.ACEPTADO:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El permiso debe estar aprobado por RRHH primero'
                }, status=400)
            
            # Aprobar en nivel Gerencia
            permiso.tag2 = RestDays.ACEPTADO
            permiso.dt2 = timezone.now()
            
            if comentario:
                permiso.motive = f"{permiso.motive}\nAprobado por Gerencia: {comentario}"
            
            permiso.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Permiso aprobado por Gerencia'
            })
            
        except RestDays.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Permiso no encontrado'
            }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class DenegarPermisoGerenciaView(LoginRequiredMixin, View):
    """Vista para denegación de permisos por Gerencia"""
    
    def post(self, request, *args, **kwargs):
        permiso_id = request.POST.get('permiso_id')
        comentario = request.POST.get('comentario', '')
        
        if not comentario:
            return JsonResponse({
                'status': 'error',
                'message': 'Debe ingresar un motivo de denegación'
            }, status=400)
        
        try:
            permiso = RestDays.objects.get(id=permiso_id)
            
            if request.user.position != "0":
                return JsonResponse({
                    'status': 'error',
                    'message': 'No tienes permisos para esta acción'
                }, status=403)
            
            # Denegar en nivel Gerencia
            permiso.tag2 = RestDays.DENEGADO
            permiso.dt2 = timezone.now()
            permiso.motive = permiso.motive + "/n" f"Denegado por Gerencia: {comentario}"
            permiso.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Permiso denegado por Gerencia'
            })
            
        except RestDays.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Permiso no encontrado'
            }, status=404)


# ======================= ACTIVIDAD DIARIA MODALS ===========================
class MyDailyTaskListView(LoginRequiredMixin,ListView):
    template_name = "actividades/mi-lista-actividades-diarias.html"
    model = DailyTasks
    context_object_name = 'data'

    def get_queryset(self):
        userId = self.request.user
        restTimeNoCompensate = RestDays.objects.getRestTimesNoCompensateById(userId)
        payload = {"rest": restTimeNoCompensate}
        return payload

def get_task_detail(request, task_id):
    try:
        task = DailyTasks.objects.get(id=task_id, user=request.user)
        data = {
            'id': task.id,
            'activity': task.activity,
            'type': task.type,
            'overTime': str(task.overTime) if task.overTime else '0',
            'rest_day': task.rest_day.id if task.rest_day else None,
            'date': task.date.strftime('%Y-%m-%d')
        }
        return JsonResponse(data)
    except DailyTasks.DoesNotExist:
        return JsonResponse({'error': 'Tarea no encontrada'}, status=404)
    
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = "actividades/mi-lista-actividades-diarias.html"

class DailyTasksListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tasks = DailyTasks.objects.filter(user=request.user).select_related('rest_day')
        color_map = {
            '0': '#4caf50',  # Jornada Regular
            '1': '#03a9f4',  # Horas Extra
            '2': '#fb8c00',  # Feriado
            '3': '#7b809a',  # Otro
            '4': '#8bc34a',  # Compensación
        }

        events = []
        for task in tasks:
            event = {
                'id': task.id,
                'title': task.activity or 'Sin descripción',
                'start': str(task.date),
                'color': color_map.get(task.type, '#607D8B'),
                'extendedProps': {
                    'type': task.type,
                    'overTime': str(task.overTime) if task.overTime else '0',
                    'rest_day_id': task.rest_day.id if task.rest_day else None,
                    'rest_day_info': self._get_rest_day_info(task.rest_day) if task.rest_day else None,
                    'compensation_data': self._get_compensation_data(task) if task.type == '4' else None,
                }
            }
            events.append(event)

        return JsonResponse(events, safe=False)

    def _get_rest_day_info(self, rest_day):
        """Formatea la información del día de descanso asociado"""
        if not rest_day:
            return None
            
        info = f"{rest_day.get_type_display()} - {rest_day.startDate.strftime('%d-%b-%Y')}"
        if rest_day.days:
            info += f" | {rest_day.days} días"
        if rest_day.hours:
            info += f" | {rest_day.hours} horas"
        return info

    def _get_compensation_data(self, task):
        """Obtiene datos de compensación para tareas tipo 4"""
        if not task.rest_day:
            return None
            
        return {
            'days_remaining': task.rest_day.days - task.rest_day.daysCompensated if task.rest_day.days else 0,
            'hours_remaining': float(task.rest_day.hours - Decimal(task.rest_day.hoursCompensated)) if task.rest_day.hours else 0,
            'status': task.rest_day.get_tag1_display() or task.rest_day.get_tag2_display()
        }

@method_decorator(csrf_exempt, name='dispatch')
class DailyTasksSaveView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Validar datos requeridos
            if not all([data.get("date"), data.get("type")]):
                return JsonResponse({"status": "error", "message": "Faltan campos requeridos"}, status=400)
            
            # Validar horas extra si es tipo 1
            if data.get("type") == '1':
                if not data.get("overTime"):
                    return JsonResponse({"status": "error", "message": "Las horas extra requieren cantidad de horas"}, status=400)
                try:
                    over_time = Decimal(data.get("overTime"))
                    if over_time <= 0:
                        raise ValueError
                except (TypeError, ValueError):
                    return JsonResponse({"status": "error", "message": "Horas extra debe ser un número positivo"}, status=400)
            
            # Validar permiso a compensar si es tipo 4
            rest_day = None
            if data.get("type") == '4':
                if not data.get("rest_day"):
                    return JsonResponse({"status": "error", "message": "Debe seleccionar un permiso a compensar"}, status=400)
                
                try:
                    rest_day = RestDays.objects.get(
                        id=data.get("rest_day"), 
                        user=request.user,
                        isCompensated=True
                    )
                    self._validate_rest_day_for_compensation(rest_day)
                except RestDays.DoesNotExist:
                    return JsonResponse({"status": "error", "message": "Permiso a compensar no válido o no disponible"}, status=400)
                except ValueError as e:
                    return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
            # Crear la tarea
            tarea = DailyTasks.objects.create(
                user=request.user,
                date=data.get("date"),
                activity=data.get("activity", "Actividad regular"),
                type=data.get("type"),
                overTime=Decimal(data.get("overTime")) if data.get("type") == '1' else None,
                rest_day=rest_day
            )
            
            # Si es compensación, actualizar días/horas compensados
            if data.get("type") == '4' and rest_day:
                self._apply_compensation(rest_day, data.get("overTime", 8))
            
            return JsonResponse({
                "status": "success", 
                "action": "created",
                "id": tarea.id,
                "rest_day_info": self._get_rest_day_info(rest_day) if rest_day else None,
                "compensation_data": self._get_compensation_data(tarea) if rest_day else None
            })
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Validar ID de tarea
            if not data.get("id"):
                return JsonResponse({"status": "error", "message": "ID de tarea requerido"}, status=400)
            
            # Obtener tarea existente
            tarea = DailyTasks.objects.get(id=data["id"], user=request.user)
            original_type = tarea.type
            original_rest_day = tarea.rest_day
            
            # Validar cambios según tipo
            if data.get("type") == '1':
                if not data.get("overTime"):
                    return JsonResponse({"status": "error", "message": "Las horas extra requieren cantidad de horas"}, status=400)
                try:
                    over_time = Decimal(data.get("overTime"))
                    if over_time <= 0:
                        raise ValueError
                except (TypeError, ValueError):
                    return JsonResponse({"status": "error", "message": "Horas extra debe ser un número positivo"}, status=400)
            
            # Manejar cambio de tipo a compensación
            new_rest_day = None
            if data.get("type") == '4':
                if not data.get("rest_day"):
                    return JsonResponse({"status": "error", "message": "Debe seleccionar un permiso a compensar"}, status=400)
                
                try:
                    new_rest_day = RestDays.objects.get(
                        id=data.get("rest_day"), 
                        user=request.user,
                        isCompensated=True
                    )
                    self._validate_rest_day_for_compensation(new_rest_day)
                except RestDays.DoesNotExist:
                    return JsonResponse({"status": "error", "message": "Permiso a compensar no válido o no disponible"}, status=400)
                except ValueError as e:
                    return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
            # Revertir compensación anterior si estaba en tipo 4
            if original_type == '4' and original_rest_day:
                self._revert_compensation(original_rest_day, tarea.overTime or 8)
            
            # Actualizar campos
            tarea.activity = data.get("activity", tarea.activity)
            tarea.type = data.get("type", tarea.type)
            tarea.overTime = Decimal(data.get("overTime")) if data.get("type") == '1' else None
            tarea.rest_day = new_rest_day
            tarea.save()
            
            # Aplicar nueva compensación si es tipo 4
            if data.get("type") == '4' and new_rest_day:
                self._apply_compensation(new_rest_day, data.get("overTime", 8))
            
            return JsonResponse({
                "status": "success",
                "action": "updated",
                "rest_day_info": self._get_rest_day_info(new_rest_day) if new_rest_day else None,
                "compensation_data": self._get_compensation_data(tarea) if new_rest_day else None
            })
            
        except DailyTasks.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Tarea no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tarea = DailyTasks.objects.get(id=data["id"], user=request.user)
            
            # Si es compensación, revertir los días/horas compensados
            if tarea.type == '4' and tarea.rest_day:
                self._revert_compensation(tarea.rest_day, tarea.overTime or 8)
            
            tarea.delete()
            return JsonResponse({"status": "success", "action": "deleted"})
            
        except DailyTasks.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Tarea no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    def _validate_rest_day_for_compensation(self, rest_day):
        """Valida que el RestDay sea apto para compensación"""
        if not rest_day.isCompensated:
            raise ValueError("Este permiso no requiere compensación")
            
        #if rest_day.tag1 not in [RestDays.ACEPTADO, RestDays.CREADO] or rest_day.tag2 not in [RestDays.ACEPTADO, RestDays.CREADO]:
        #    raise ValueError("El permiso no está aprobado para compensación")
        
        if rest_day.days:
            if rest_day.daysCompensated >= rest_day.days:
                raise ValueError("No quedan días por compensar en este permiso")
        elif rest_day.hours:
            if Decimal(rest_day.hoursCompensated) >= rest_day.hours:
                raise ValueError("No quedan horas por compensar en este permiso")
        else:
            raise ValueError("El permiso no tiene días/horas definidos para compensar")

    def _apply_compensation(self, rest_day, hours=8):
        """Aplica la compensación al RestDay"""
        if rest_day.days:
            rest_day.daysCompensated = (rest_day.daysCompensated or 0) + 1
        elif rest_day.hours:
            hours_to_add = Decimal(hours)
            rest_day.hoursCompensated = (rest_day.hoursCompensated or 0) + float(hours_to_add)
        
        rest_day.save()

    def _revert_compensation(self, rest_day, hours=8):
        """Revierte la compensación del RestDay"""
        if rest_day.days and rest_day.daysCompensated > 0:
            rest_day.daysCompensated -= 1
        elif rest_day.hours and rest_day.hoursCompensated > 0:
            hours_to_remove = float(Decimal(hours))
            rest_day.hoursCompensated = max(0, rest_day.hoursCompensated - hours_to_remove)
        
        rest_day.save()

    def _get_rest_day_info(self, rest_day):
        """Helper para formatear la información del RestDay"""
        if not rest_day:
            return None
        info = f"{rest_day.get_type_display()} - {rest_day.startDate.strftime('%d-%b-%Y')}"
        if rest_day.days:
            info += f" | {rest_day.days}d ({rest_day.daysCompensated}c)"
        if rest_day.hours:
            info += f" | {rest_day.hours}h ({rest_day.hoursCompensated}c)"
        return info

    def _get_compensation_data(self, task):
        """Obtiene datos de compensación para la respuesta"""
        if not task.rest_day:
            return None
            
        return {
            'days_remaining': task.rest_day.days - task.rest_day.daysCompensated if task.rest_day.days else None,
            'hours_remaining': float(task.rest_day.hours - Decimal(task.rest_day.hoursCompensated)) if task.rest_day.hours else None,
            'status': self._get_rest_day_status(task.rest_day)
        }

    def _get_rest_day_status(self, rest_day):
        """Obtiene el estado del RestDay"""
        if rest_day.tag1 == RestDays.ACEPTADO and rest_day.tag2 == RestDays.ACEPTADO:
            return "Aprobado"
        return "Pendiente de aprobación"

# ======================= BUZON DE SUGERENCIAS ===========================
class MySuggestionBoxListView(LoginRequiredMixin,ListView):
    template_name = "actividades/mi-buzon-de-sugerencias.html"
    context_object_name = 'buzon'
    #model = SuggestionBox

    def get_queryset(self):
        payload = {}
        payload["suggestion"] = SuggestionBox.objects.MiListaDeSugerencias(user=self.request.user)
        return payload

class SuggestionBoxCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/crear-buzon-de-sugerencias.html"
    model = SuggestionBox
    form_class = SuggestionBoxForm
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')

class SuggestionBoxUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "actividades/editar-buzon-de-sugerencias.html"
    model = SuggestionBox
    form_class = SuggestionBoxForm
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')

class SuggestionBoxDeleteView(LoginRequiredMixin,DeleteView):
    template_name = "actividades/eliminar-sugerencia.html"
    model = SuggestionBox
    success_url = reverse_lazy('activities_app:mi-buzon-de-sugerencias')
    

# ======================= COTIZACIONES TRANSFORMADORES ===========================
class QuotesListView(LoginRequiredMixin,ListView):
    template_name = "actividades/lista-cotizaciones-transformadores.html"
    context_object_name = 'cotizaciones'
    
    def get_queryset(self):
        intervalDate = self.request.GET.get("dateKword", '')
        if intervalDate == "today" or intervalDate =="":
            intervalDate = str(date.today() - timedelta(days = 30)) + " to " + str(date.today())
        
        quotes = TrafoQuote.objects.ListarPorIntervalo(interval=intervalDate)
        #trafos = Trafos.objects.ListaPorCotizaciones(quotes=quotes)

        dictResult = {}
        for i in quotes:
            dictResult[i] =  Trafos.objects.ListaPorCotizaciones(quote=i.id)
        
        payload = {}
        payload["intervalDate"] = intervalDate
        payload["data"] = dictResult
            
        return payload

class QuotesCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/cotizaciones-transformadores-nuevo.html"
    form_class = QuoteTrafoForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesEditView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/cotizaciones-transformadores-editar.html"
    model = TrafoQuote
    form_class = QuoteTrafoForm
     
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDeleteView(ProduccionPermisoMixin,DeleteView):
    template_name = "actividades/cotizaciones-transformadores-eliminar.html"
    model = TrafoQuote
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

class QuotesDetailView(LoginRequiredMixin,ListView):
    template_name = "actividades/cotizaciones-transformadores-detalle.html"
    context_object_name = 'data'

    #model = TrafoQuote

    def get_queryset(self,**kwargs):
        pk = self.kwargs['pk']
        payload = {}
        quotation = TrafoQuote.objects.CotizacionPorId(id = int(pk))
        trafos = Trafos.objects.ListaPorCotizaciones(quotation.id)
        tasks = TrafoTask.objects.ListaTareasPorCotizacion(quotation.id)
        payload["quotation"] = quotation
        payload["trafos"] = trafos
        payload["tasks"] = tasks
        return payload

class TrafoCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/crear-transformador.html"
    model = Trafos
    form_class = TrafoForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_context_data(self, **kwargs):
        context = super(TrafoCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context

class TrafoUpdateView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/editar-transformador.html"
    model = Trafos
    form_class = TrafoForm

    def get_success_url(self, *args, **kwargs):
        #print(self.object.TrafoQuote)
        pk = self.object.idQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

class TrafoDeleteView(ProduccionPermisoMixin,DeleteView):
    template_name = "actividades/eliminar-transformador.html"
    model = Trafos
    def get_success_url(self, *args, **kwargs):
        pk = self.object.idQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

class TaskQuotesTrafoCreateView(ProduccionPermisoMixin,CreateView):
    template_name = "actividades/agregar-tareas-orden-transformador.html"
    model = TrafoTask
    form_class = TrafoTaskForm
    #success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_success_url(self, *args, **kwargs):
        print(self.object.idTrafoQuote)
        pk = self.object.idTrafoQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(TaskQuotesTrafoCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context
    
class TaskQuotesTrafoUpdateView(ProduccionPermisoMixin,UpdateView):
    template_name = "actividades/editar-tareas-orden-transformador.html"
    model = TrafoTask
    form_class = TrafoTaskForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_success_url(self, *args, **kwargs):
        pk = self.object.idTrafoQuote.id
        return reverse_lazy('activities_app:cotizaciones-transformadores-detalle', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super(TaskQuotesTrafoUpdateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.object.idTrafoQuote.id)
        context['quotation'] = trafoQuote
        return context

# ========================== EMAILS ==========================
class InitialEmailCreateView(LoginRequiredMixin,CreateView):
    template_name = "actividades/initial-email.html"
    model = EmailSent
    form_class = EmailSentForm
    success_url = reverse_lazy('activities_app:cotizaciones-transformadores')

    def get_context_data(self, **kwargs):
        context = super(InitialEmailCreateView, self).get_context_data(**kwargs)
        trafoQuote = TrafoQuote.objects.get(id = self.kwargs['pk'])
        context['quotation'] = trafoQuote
        return context

