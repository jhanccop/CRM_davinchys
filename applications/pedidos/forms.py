# django
from django import forms
# local
from .models import (
    RequestList,
    PaymentRequest
)

from applications.clientes.models import Cliente

class ListRequestForm(forms.ModelForm):
    class Meta:
        model = RequestList
        fields = (
            'listName',
            'idPetitioner',
        )
        
        widgets = {
            'listName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idPetitioner': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = (
            'idPetitioner',
            'idList',

            'requirementName',

            'quantity',
            'amountRequested',
            'idProvider',

            'currencyType',
            'deadline',

            'paymentType',
            'idCommissions',
            'idProjects',
            'idTrafoOrder',
            'pdf_file'
        )
        
        widgets = {
            'idPetitioner': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idList': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idProvider': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'requirementName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'quantity': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'text-center form-control',
                }
            ),
            'amountRequested': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'text-center form-control',
                }
            ),
            'amountAssigned': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'text-center form-control',
                }
            ),
            'paymentType': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'currencyType': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idCommissions': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idProjects': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idTrafoOrder': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'pdf_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"pdf_file",
                    'class': 'form-control text-dark',
                    'id':"id_pdf_file",
                }
            ),
            #'idSupervisor': forms.SelectMultiple(
            #    attrs = {
            #        'class': 'form-control choices__input',
            #    }
            #),
        }
    
    #def __init__(self, *args, **kwargs):
    #    super(PaymentRequestForm, self).__init__(*args, **kwargs)
    #    self.fields['idSupervisor'].queryset = User.objects.filter(position__in = ['0','3'])
    
    def clean_amount(self):
        amountRequested = self.cleaned_data['amountRequested']
        if not amountRequested > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amountRequested

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf') and not pdf_file.name.endswith('.png') and not pdf_file.name.endswith('.jpg') and not pdf_file.name.endswith('.jpeg'):
                raise forms.ValidationError("Archivos permitidos pdf, png, jpg y jpeg.")
            if pdf_file.size > 1*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 1 MB.")
        return pdf_file

class ApprovePaymentRequestForm1(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = (
            'amountAssigned',
            'observations',
            'tag1',
            'typeRequest',
            'tag2',
            'tag3',
            'tag4',
        )
        
        widgets = {
            'amountAssigned': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'observations': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'typeRequest': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'onchange':"toggleDiv0()"
                }
            ),
            'tag1': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'onchange':"toggleDiv0()"
                }
            ),
            'tag2': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'onchange':"toggleDiv2()"
                }
            ),
            'tag3': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                    'onchange':"toggleDiv3()"
                }
            ),
            'tag4': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ApprovePaymentRequestForm1, self).__init__(*args, **kwargs)
        choices = (
            ("4", "--------"),
            ("0",""),
            ("1", "aceptado"),
            ("2", "denegado"),
            ("3", "observado")
        )
        self.fields['tag1'].choices = choices
        self.fields['tag2'].choices = choices
        self.fields['tag3'].choices = choices
        self.fields['tag4'].choices = choices

    def clean_amount(self):
        amountAssigned = self.cleaned_data['amountAssigned']
        if not amountAssigned > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amountAssigned
