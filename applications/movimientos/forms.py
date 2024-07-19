# django
from django import forms
# local
from .models import (
  InternalTransfers,
  BankMovements,
  BankReconciliation
)

class InternalTransfersForm(forms.ModelForm):
    class Meta:
        model = InternalTransfers
        fields = [
            'idSourceAcount',
            'idDestinationAcount',
            'SourceAmount',
            'DestinationAmount',
            'opNumber',
        ]
        widgets = {
            'idSourceAcount': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idDestinationAcount': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'SourceAmount': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'DestinationAmount': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'opNumber': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
                        
            
        }

class BankMovementsForm(forms.ModelForm):
    class Meta:
        model = BankMovements
        fields = [
            'idAccount',
            'date',
            'description',
            'amount',
            'opNumber',
        ]
        widgets = {
                'idAccount': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
                'date': forms.DateInput(
                    format='%Y-%m-%d',
                    attrs = {
                        'placeholder': '',
                        'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                    }
                ),
                'description': forms.TextInput(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
                'amount': forms.NumberInput(
                    attrs = {
                        'class': 'input-group-field form-control',
                    }
                ),
                'opNumber': forms.TextInput(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
                            
                
            }
        
class BankReconciliationForm(forms.ModelForm):
    class Meta:
        model = BankReconciliation
        fields = [
            # oculto
            'user',
            'idBankMovements',

            # generales
            'incomeCategory',
            'expensesCategory',

            'date',
            'typeInvoice',
            'idInvoice',
            'annotation',

            'idClient',
            'amountReconcilied',

            'description',
            
            'ActivitiesCategory',
            'idTrafoOrder',
            'idCommission',
            'idProject',
            
            'subCategoryPallRoy',
            'subCategoryCashBox',
            
            'contabilidad',
            'pdf_file'
            
        ]
        widgets = {
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
            # =======================
            'idClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'amountReconcilied': forms.NumberInput(
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
            'ActivitiesCategory': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDivActivities()"
                }
            ),

            'idTrafoOrder': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'idCommission': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'idProject': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),

            # =======================
            'expensesCategory': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            
            'subCategoryCashBox': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'subCategoryPallRoy': forms.Select(
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
                    'onchange':"toggleDiv()"
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
        
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        if not amountReconcilied > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amountReconcilied

class DocReconciliationUpdateForm(forms.ModelForm):
    class Meta:
        model = BankReconciliation
        fields = [
            # oculto
            'user',
            'idBankMovements',

            # generales
            'incomeCategory',
            'expensesCategory',

            'date',
            'typeInvoice',
            'idInvoice',
            'annotation',

            'idClient',
            'amountReconcilied',

            'description',
            
            'ActivitiesCategory',
            'idTrafoOrder',
            'idCommission',
            'idProject',
            
            'subCategoryPallRoy',
            'subCategoryCashBox',
            
            'contabilidad',
            'pdf_file'
            
        ]
        widgets = {

            'idBankMovements': forms.SelectMultiple(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control w-100',
                    #'disabled': True
                }
            ),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'typeInvoice': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
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
            # =======================
            'idClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'amountReconcilied': forms.NumberInput(
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
            'ActivitiesCategory': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDivActivities()"
                }
            ),

            'idTrafoOrder': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'idCommission': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            'idProject': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),

            # =======================
            'expensesCategory': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange':"toggleDiv()"
                }
            ),
            
            'subCategoryCashBox': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'subCategoryPallRoy': forms.Select(
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
                    'onchange':"toggleDiv()"
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
    
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        if not amountReconcilied > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amountReconcilied
  
class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Sellecionar archivo:",
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control bg-gradient-secondary text-dark',
                'type': 'file',
                'id':"formFile"
                }
        )
    )

