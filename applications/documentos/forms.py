# django
from django import forms
# local
from .models import (
  FinancialDocuments,
  OthersDocuments
)

class FinancialDocumentsForm(forms.ModelForm):
    class Meta:
        model = FinancialDocuments
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

            'description',
            
            'contabilidad',
            'pdf_file'
            
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
            # =======================
            'description': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
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
        }
        
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not amount > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amount
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if pdf_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return pdf_file
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FinancialDocumentsForm, self).__init__(*args, **kwargs)

        if self.request:
            self.fields['idTin'].initial = self.request.session['compania_id']

class OthersDocumentsForm(forms.ModelForm):
    class Meta:
        model = OthersDocuments
        fields = [
            # oculto
            'user',

            # generales
            'typeDoc',
            'date',
            'idFinacialDocuments',
            'description',
            'idOtherDocument',
            'amount',
            

            'pdf_file',
            
        ]
        widgets = {
            'typeDoc': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDivtypeDoc()"
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'idFinacialDocuments': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDividFinacialDocuments()"
                }
            ),
            'description': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idOtherDocument': forms.TextInput(
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
                }
            ),
        }
        
    #def clean_amount(self):
    #    amount = self.cleaned_data['amount']
    #    if not amount > 0:
    #        raise forms.ValidationError('Ingrese un monto mayor a cero')
    #    return amount
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError("Archivos permitidos pdf")
            if pdf_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return pdf_file
    
    
