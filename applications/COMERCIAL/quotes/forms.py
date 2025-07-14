from django import forms
# local
from .models import (
  Trafos,
  TrafoQuote,
)

from django.forms import inlineformset_factory

from applications.users.models import User

class TrafoQuoteForm(forms.ModelForm):
    class Meta:
        model = TrafoQuote
        fields = (
            'idQuote',
            'idTin',
            'idClient',

            'dateOrder',
            'deadline',

            'currency',
            'amount',
            'payMethod',
            
            'idAttendant',
            'description',
            'poStatus',
            'currency',
            'payMethod'
        )
        
        widgets = {
            'idQuote': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'userClient': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'dateOrder': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'idAttendant': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'rows':2,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'poStatus': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
            ),
            'currency': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'amount': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'payMethod': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TrafoQuoteForm, self).__init__(*args, **kwargs)
        self.fields['idAttendant'].queryset = User.objects.filter(position = "2")

class TrafoForm(forms.ModelForm):
    class Meta:
        model = Trafos
        fields = (
            'idTrafoQuote',

            #'provider',
            'quantity',
            'unitCost',

            'KVA',
            'HVTAP',
            'KTapHV',
            'FIXHV',

            'LV',
            'HZ',
            'TYPE',
            'MOUNTING',

            'COOLING',
            'WINDING',
            'INSULAT',
            'CONNECTION',

            'STANDARD',

        )
        widgets = {
            
            'unitCost': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'quantity': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'KVA': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'HVTAP': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'KTapHV': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'FIXHV': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'LV': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'HZ': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'TYPE': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'MOUNTING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'COOLING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'WINDING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'INSULAT': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'CONNECTION': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'STANDARD': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'rows': '3',
                    'class': 'input-group-field form-control',
                }
            )
        }

TrafosFormSet = inlineformset_factory(
    TrafoQuote,
    Trafos,
    form=TrafoForm,
    extra=1,
    can_delete=True,
    fields='__all__'
)
