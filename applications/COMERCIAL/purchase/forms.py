from django import forms

from django.core.exceptions import ValidationError

from django.forms import inlineformset_factory
from .models import (
    requirements,
    requirementItems,
    PettyCash,
    PettyCashItems,
    requirementsInvoice
)

# ============================ REQUERIMENTOS ============================
class RequirementsForm(forms.ModelForm):
    class Meta:
        model = requirements
        fields = [
            'idPetitioner',
            'description',
            'currency',
            'totalPrice'
        ]

        widgets = {
            'idPetitioner': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'currency': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'totalPrice': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }

class RequirementItemForm(forms.ModelForm):
    class Meta:
        model = requirementItems
        fields = [
            'idRequirement',
            'product',
            'quantity',
            'price',
        ]

        widgets = {
            'idRequirement': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'product': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'quantity': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }

# ============================ CAJA CHICA ============================
class PettyCashForm(forms.ModelForm):
    class Meta:
        model = PettyCash
        fields = [
            'idPetitioner',
            'description',
            'currency',
            'totalPrice'
        ]

        widgets = {
            'idPetitioner': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'currency': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'totalPrice': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }

class PettyCashItemForm(forms.ModelForm):
    class Meta:
        model = PettyCashItems
        fields = [
            'idPettyCash',
            'product',
            'quantity',
            'price',
            'category'
        ]

        widgets = {
            'idPettyCash': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'product': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'quantity': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'category': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }


class requirementsInvoiceForm(forms.ModelForm):
    class Meta:
        model = requirementsInvoice
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

            'idSupplier',
            'typeCurrency',
            'amount',
            'netAmount',
            'incomeTax',

            'description',
            'shortDescription',
            'declareFlag',
            
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
            'idSupplier': forms.Select(
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
        super(requirementsInvoiceForm, self).__init__(*args, **kwargs)

        self.fields['xml_file'].widget.attrs.update({
            'accept': '.xml',
            'class': 'form-control'
        })

        if self.request:
            self.fields['idTin'].initial = self.request.session['compania_id']
