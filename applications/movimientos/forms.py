# django
from django import forms
# local
from .models import (
  InternalTransfers,
  BankMovements,
  Documents
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

class ConciliationDocumentsForm(forms.ModelForm):
    class Meta:
        model = BankMovements
        fields = [
            'idDocs'
        ]
        widgets = {
                'idDocs': forms.SelectMultiple(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control w-100',
                       #'disabled': True
                    }
                ),
            }
        
    def __init__(self, *args, **kwargs):
        super(ConciliationDocumentsForm, self).__init__(*args, **kwargs)
        self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class ConciliationBankMovementsForm(forms.ModelForm):
    class Meta:
        model = BankMovements
        fields = [
            'idMovement',
            'amountReconcilied',
            'conciliationType',
        ]
        widgets = {
                'idMovement': forms.SelectMultiple(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control w-100',
                       #'disabled': True
                    }
                ),
                'amountReconcilied': forms.NumberInput(
                    attrs = {
                        'class': 'input-group-field form-control',
                    }
                ),
                'conciliationType': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
            }
        
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        if not amountReconcilied >= 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero.')
        return amountReconcilied

    def clean_idMovement(self):
        idMovement = self.cleaned_data['idMovement']
        print(idMovement)
        if len(idMovement) > 1:
            raise forms.ValidationError('Ingrese solo un movimiento de destino.')
        return idMovement
    
    def __init__(self, *args, **kwargs):
        super(ConciliationBankMovementsForm, self).__init__(*args, **kwargs)
        idAccount = kwargs['instance'].idAccount.id
        print(idAccount)
        #self.fields['idMovement'].queryset = BankMovements.objects.exclude(idDocs__isnull = False)
        self.fields['idMovement'].queryset = BankMovements.objects.exclude(idAccount__id = idAccount)

class BankMovementsForm(forms.ModelForm):
    class Meta:
        model = BankMovements
        fields = [
            'idAccount',
            'date',
            'description',
            'amount',
            'opNumber',
            'transactionType'
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
                'transactionType': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
                            
                
            }

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = [
            # oculto
            'user',

            # generales
            'incomeCategory',
            'expensesCategory',

            'date',
            'typeInvoice',
            'idInvoice',
            'annotation',

            'month_dec',
            'year_dec',

            'idClient',
            'typeCurrency',
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
        model = Documents
        fields = [
            # oculto
            'user',
            #'idBankMovements',

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

            #'idBankMovements': forms.SelectMultiple(
            #    attrs = {
            #        'placeholder': '',
            #        'class': 'input-group-field form-control w-100',
                    #'disabled': True
            #    }
            #),
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

