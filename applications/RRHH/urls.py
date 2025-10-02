# urls.py
from django.urls import path
from . import views

app_name = 'rrhh_app'

urlpatterns = [
    # Dashboard
    path('rrhh/dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('rrhh/reporte-asistencia-persona/', views.ReporteAsistenciaPersonaView.as_view(), name='reporte_asistencia_persona'),

    # myspace
    path('rrhh/registro-rapido/', views.RegistroAsistenciaRapidoView.as_view(), name='registro_asistencia_rapido'),
    path('rrhh/horas-extra/<str:tipo_extra>/', views.RegistroHorasExtraView.as_view(), name='registro_horas_extra'),
    
    # Empleados
    path('rrhh/empleados/', views.EmpleadoListView.as_view(), name='empleados-list'),
    path('rrhh/empleado/<int:pk>/', views.EmpleadoDetailView.as_view(), name='empleado-detail'),
    path('rrhh/empleado/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado-create'),
    path('rrhh/empleado/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado-update'),
    path('rrhh/empleado/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado-delete'),
    
    # Contactos de Emergencia
    path('rrhh/contacto/nuevo/', views.ContactoEmergenciaCreateView.as_view(), name='contacto-create'),
    path('rrhh/contacto/<int:pk>/editar/', views.ContactoEmergenciaUpdateView.as_view(), name='contacto-update'),
    path('rrhh/contacto/<int:pk>/eliminar/', views.ContactoEmergenciaDeleteView.as_view(), name='contacto-delete'),
    
    # Asistencia
    path('rrhh/asistencia/', views.AsistenciaListView.as_view(), name='asistencia-list'),
    path('rrhh/asistencia/registrar/', views.AsistenciaCreateView.as_view(), name='asistencia-create'),
    path('rrhh/asistencia/<int:pk>/editar/', views.AsistenciaUpdateView.as_view(), name='asistencia-update'),
    path('rrhh/asistencia/<int:pk>/eliminar/', views.AsistenciaDeleteView.as_view(), name='asistencia-delete'),

    path('rrhh/mi-asistencia/', views.AsistenciaUserListView.as_view(), name='asistencia-user-list'),
    path('rrhh/mi-asistencia/registrar/', views.AsistenciaCreateUserView.as_view(), name='asistencia-user-create'),
    path('rrhh/mi-asistencia/<int:pk>/editar/', views.AsistenciaUpdateUserView.as_view(), name='asistencia-user-update'),
    path('rrhh/mi-asistencia/<int:pk>/eliminar/', views.AsistenciaDeleteUserView.as_view(), name='asistencia-user-delete'),

    path('rrhh/asistencia/usuario/', views.RegistroAsistenciaRapidoView.as_view(), name='registro_asistencia_rapido'),
    path('rrhh/asistencia/horas-extra/<str:tipo>/', views.RegistroHorasExtraView.as_view(), name='registro_horas_extra'),
    
    # Documentos
    path('rrhh/documentos/', views.DocumentoListView.as_view(), name='documentos-list'),
    path('rrhh/documentos/subir/', views.DocumentoCreateView.as_view(), name='documento-create'),
    path('rrhh/documentos/editar/<int:pk>/', views.DocumentoUpdate.as_view(), name='documento-update'),
    path('rrhh/documentos/eliminar/<int:pk>/', views.DocumentoDeleteView.as_view(), name='documento-delete'),

    path('rrhh/mis-documentos/', views.DocumentoUserListView.as_view(), name='mis-documentos'),
    path('rrhh/mis-documentos/registrar/', views.DocumentoCreateUserView.as_view(), name='mis-documentos-registrar'),
    path('rrhh/mis-documentos/editar/<int:pk>/', views.DocumentoUpdateUserView.as_view(), name='mis-documentos-update'),
    path('rrhh/mis-documentos/eliminar/<int:pk>/', views.DocumentoDeleteUserView.as_view(), name='mis-documentos-delete'),

]