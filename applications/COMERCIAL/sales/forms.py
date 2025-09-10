from django import forms

from django.core.exceptions import ValidationError

from .models import (
  Incomes,
  Trafos,
  quotes,
)
from django.forms import inlineformset_factory
from applications.users.models import User

class IncomesForm(forms.ModelForm):
    class Meta:
        model = Incomes
        fields = [
            # oculto
            'user',

            # generales
            'idTin',
            'date',
            'typeInvoice',
            'idInvoice',
            'annotation',

            'detraction',
            'shippingGuide',
            'retention',
            'month_dec',
            'year_dec',

            'idClient',
            'typeCurrency',
            'amount',
            'netAmount',
            'incomeTax',

            'description',
            'shortDescription',
            'declareFlag',
            
            'contabilidad',
            'xml_file',
            'pdf_file',
            
        ]
        widgets = {
            'idTin': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'readonly':True
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'typeInvoice': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDivTypeInvoice()"
                }
            ),
            'idInvoice': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'annotation': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'detraction': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'shippingGuide': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'retention': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'month_dec': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'year_dec': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            # =======================
            'idClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'typeCurrency': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'amount': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control text-center',
                }
            ),
            'incomeTax': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control text-center',
                }
            ),
            'netAmount': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control text-center',
                }
            ),
            # =======================
            'description': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'rows':4
                }
            ),
            'shortDescription': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'declareFlag': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
            ),

            # =======================
            'contabilidad': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',

                }
            ),
            'pdf_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"pdf_file",
                    'class': 'form-control text-dark',
                    'id':"id_pdf_file",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
            'xml_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"xml_file",
                    'class': 'form-control text-dark',
                    'id':"id_xml_file",
                    'accept':".xml"
                }
            ),
        }
        
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(IncomesForm, self).__init__(*args, **kwargs)

        self.fields['xml_file'].widget.attrs.update({
            'accept': '.xml',
            'class': 'form-control'
        })

        if self.request:
            self.fields['idTin'].initial = self.request.session['compania_id']

# =========================== TRAFO QUOTES ===========================

class quotesForm(forms.ModelForm):
    class Meta:
        model = quotes
        fields = (
            'idTinReceiving',
            'idTinExecuting',
            'idClient',

            'dateOrder',
            'deadline',

            'currency',
            'initialAmount',
            'amount',
            'payMethod',
            
            'shortDescription',
            'isPO',
        )
        
        widgets = {
            'idTinReceiving': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idTinExecuting': forms.Select(
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
            'shortDescription': forms.Textarea(
                attrs = {
                    'rows':2,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'isPO': forms.CheckboxInput(
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
            'initialAmount': forms.NumberInput(
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

    #def __init__(self, *args, **kwargs):
    #    super(quotesForm, self).__init__(*args, **kwargs)
    #    self.fields['idAttendant'].queryset = User.objects.filter(position = "2")

class TrafoForm(forms.ModelForm):
    class Meta:
        model = Trafos
        exclude = ['idTrafoQuote']
        fields = (
            #'idTrafoQuote',
            'serialNumber',

            #'provider',
            'quantity',
            'unitCost',

            'KVA',
            'HVTAP',
            'KTapHV',
            'LV',
            
            'FIXHV',
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
            'serialNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: hacer que el campo esté completamente ausente del formulario
        if 'idTrafoQuote' in self.fields:
            del self.fields['idTrafoQuote']

class TrafoItemForm(forms.ModelForm):
    class Meta:
        model = Trafos
        fields = (
            'idTrafoQuote',
            'serialNumber',

            #'provider',
            'quantity',
            'unitCost',

            'KVA',
            'HVTAP',
            'KTapHV',
            'LV',
            
            'FIXHV',
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
            'idTrafoQuote': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'serialNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
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
    quotes,
    Trafos,
    form=TrafoForm,
    extra=1,
    can_delete=True,
    fields='__all__'
)
