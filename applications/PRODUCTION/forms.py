from django import forms
from .models import Trafos

class TrafosForm(forms.ModelForm):
    class Meta:
        model = Trafos
        fields = [
            'idSupplier', 'DERIVATIONS','KVA','HV', 'LV', 'HZ', 
            'PHASE', 'MOUNTING', 'COOLING', 'WINDING', 
            'CONNECTION', 'STANDARD','KTAPSVALUES'
        ]
        widgets = {
            'idSupplier': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'KVA': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2',
                #'data-placeholder': 'Seleccionar kVA'
            }),
            'HV': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'LV': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'HZ': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'PHASE': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'MOUNTING': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'COOLING': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'DERIVATIONS': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'WINDING': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'CONNECTION': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'STANDARD': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'KTAPSVALUES': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 10, 20, 30, 40'
            }),
        }
        labels = {
            'idSupplier': 'Proveedor',
            'KVA': 'Capacidad kVA',
            'HV': 'Tap HV',
            'LV': 'LV',
            'HZ': 'Frecuencia',
            'PHASE': 'Fases',
            'MOUNTING': 'Tipo de Montaje',
            'COOLING': 'Enfriamiento',
            'WINDING': 'Devanado',
            'INSULAT': 'Clase de Aislamiento',
            'CONNECTION': 'Conexión',
            'STANDARD': 'Estándar',
            'KTAPSVALUES': "Lista Ktaps"
        }

class TrafosFilterForm(forms.Form):
    KVA = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Trafos.KVA_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    TYPE = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Trafos.PHASE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    MOUNTING = forms.ChoiceField(
        choices=[('', 'Todos')] + list(Trafos.MOUNTING_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )