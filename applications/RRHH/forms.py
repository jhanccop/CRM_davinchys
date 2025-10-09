# forms.py
from django import forms
from .models import *

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha_contratacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo_contrato': forms.Select(attrs={
                'class': 'form-control',
            }),
            'moneda': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salario_base': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            
        }

class ContactoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = ContactoEmergencia
        fields = ['nombre', 'parentesco', 'telefono', 'email', 'direccion', 'principal']
        widgets = {
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }

class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = ['empleado','fecha','hora_inicio','hora_final','idLocal','observaciones']
        widgets = {
            'empleado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                'class': 'form-control datetimepicker',
                'type': 'date'
            }),
            'hora_inicio': forms.TimeInput(
                format='%H:%M',
                attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hora_final': forms.TimeInput(
                format='%H:%M',
                attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'idLocal': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required':'required',
                    'required':True
                },
                
            ),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 1
            }),
        }

    #ubicacion = forms.CharField(required=True)

class FiltroAsistenciaForm(forms.Form):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        required=False,
        empty_label="Todos los empleados"
    )
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + RegistroAsistencia.TIPO_ESTADOS,
        required=False
    )
    jornada_horaria = forms.ChoiceField(
        choices=[('', 'Todas las jornadas')] + RegistroAsistencia.TIPO_JORNADA_HORARIA,
        required=False
    )
    jornada_diaria = forms.ChoiceField(
        choices=[('', 'Todas las jornadas')] + RegistroAsistencia.TIPO_JORNADA_DIARIA,
        required=False
    )
    ubicacion = forms.ChoiceField(
        choices=[('', 'Todas las ubicaciones')]
    )

class ActividadDiariaForm(forms.ModelForm):
    class Meta:
        model = ActividadDiaria
        fields = ['fecha', 'descripcion', 'horas_trabajadas', 'proyecto', 'completada']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
            'fecha_contratacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['tipo', 'fecha_inicio', 'fecha_fin', 'tipo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tipo': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = "__all__"
        widgets = {
            'empleado': forms.Select(attrs={
                'class': 'form-control',
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'fecha_documento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                'class': 'form-control datetimepicker',
                'type': 'date'
            }),
            'archivo': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"pdf_file",
                    'class': 'form-control text-dark',
                    'id':"id_archivo",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2
            }),
        }