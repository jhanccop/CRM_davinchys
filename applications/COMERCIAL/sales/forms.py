from django import forms

from django.core.exceptions import ValidationError

from .models import (
    Incomes,
    quotes,
    Items,
    ItemTracking
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
                    'class': 'form-control',
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

        labels = {
            'idClient': 'Cliente',
            'idTinReceiving': 'Empresa receptora',
            'idTinExecuting': 'Empresa ejecutora',
            'shortDescription': 'Descripción',
            'currency': 'Moneda',
            'dateOrder': 'Fecha de solicitud',
            'deadline': 'Fecha de entrega',
            'payMethod': 'Método de pago',
            'isPO': '¿Es PO?',
        }

    #def __init__(self, *args, **kwargs):
    #    super(quotesForm, self).__init__(*args, **kwargs)
    #    self.fields['idAttendant'].queryset = User.objects.filter(position = "2")

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = (
            'idTrafoQuote',
            'idTrafo',
            'seq',
            'unitCost',

        )
        widgets = {
            'idTrafoQuote': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'idTrafo': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'seq': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'unitCost': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'step': '0.01',
                    'min': '0'
                }
            ),
        }

class ItemTrackingForm(forms.ModelForm):
    class Meta:
        model = ItemTracking
        fields = (
            'idItem',
            'statusItem',
            'statusPlate',

        )
        widgets = {
            'idItem': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'statusItem': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'statusPlate': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

#ItemsFormSet = inlineformset_factory(
#    quotes,
#    Items,
#    #Trafos,
#    form=TrafoForm,
#    extra=1,
#    can_delete=True,
#    fields='__all__'
#)
