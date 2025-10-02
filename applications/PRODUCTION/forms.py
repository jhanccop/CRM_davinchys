from django import forms
from .models import Trafos

class TrafosForm(forms.ModelForm):
    class Meta:
        model = Trafos
        fields = [
            'idSupplier', 'KVA', 'HVTAP', 'KTapHV', 'FIXHV', 'LV', 'HZ', 
            'TYPE', 'MOUNTING', 'COOLING', 'WINDING', 'INSULAT', 
            'CONNECTION', 'STANDARD'
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
            'HVTAP': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'KTapHV': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'FIXHV': forms.Select(attrs={
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
            'TYPE': forms.Select(attrs={
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
            'WINDING': forms.Select(attrs={
                'class': 'form-control',
                #'data-control': 'select2'
            }),
            'INSULAT': forms.Select(attrs={
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
        }
        labels = {
            'idSupplier': 'Proveedor',
            'KVA': 'Capacidad kVA',
            'HVTAP': 'Tap HV',
            'KTapHV': 'K Tap HV',
            'FIXHV': 'FIX HV',
            'LV': 'LV',
            'HZ': 'Frecuencia',
            'TYPE': 'Tipo de Fase',
            'MOUNTING': 'Tipo de Montaje',
            'COOLING': 'Enfriamiento',
            'WINDING': 'Devanado',
            'INSULAT': 'Clase de Aislamiento',
            'CONNECTION': 'Conexión',
            'STANDARD': 'Estándar',
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