# django
from django import forms
# local
from .models import (
  InternalTransfers,
  BankMovements,
  Documents,
  Conciliation
)

from django.db.models import F

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
            'idDocs',
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
        
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        if not amountReconcilied >= 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero.')
        return amountReconcilied
        
    def __init__(self, *args, **kwargs):
        super(ConciliationDocumentsForm, self).__init__(*args, **kwargs)
        self.fields['idDocs'].queryset = Documents.objects.filter(amount__gt = F('amountReconcilied'))
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class ConciliationMovDocForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idDoc',
            'amountReconcilied',
            'exchangeRate',
            'status'
        ]
        widgets = {
                'idDoc': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control w-100',
                        #'disabled': True
                    }
                ),
                'type': forms.Select(
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
                'exchangeRate': forms.NumberInput(
                    attrs = {
                        'class': 'input-group-field form-control',
                    }
                ),
                'status': forms.CheckboxInput(
                    attrs = {
                        'class': 'form-check-input',
                        'type':"checkbox"
                        #'disabled': True
                    }
                ),
            }
        
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        #doc = self.cleaned_data['idDoc'] # self.cleaned_dataget("idDoc",None)
        doc = self.cleaned_data.get("idDoc",None)
        if doc == None:
            raise forms.ValidationError('Primero ingrese un documento.')

        movOrigin = self.cleaned_data['idMovOrigin']
        amountOrigin = BankMovements.objects.get(id = movOrigin.id)
        Doc = Documents.objects.get(id = doc.id)
        AmountDoc = Doc.amount

        accIdDoc = Conciliation.objects.SumaMontosConciliadosPorDocumentos(doc.id)
        accIdDocSum = 0 if accIdDoc["sum"] is None else accIdDoc["sum"]

        if amountReconcilied <= 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero.')
        
        diffAmountAmountReconcilied = amountOrigin.amount - amountOrigin.amountReconcilied
        if amountReconcilied > diffAmountAmountReconcilied:
            raise forms.ValidationError(f'El monto máximo a conciliar es {diffAmountAmountReconcilied}')
        
        diffAmountDocaccIdDocSum = AmountDoc - accIdDocSum
        if amountReconcilied > diffAmountDocaccIdDocSum:
            raise forms.ValidationError(f'El monto supera al saldo en el documento. {diffAmountDocaccIdDocSum}')
        
        return amountReconcilied
    
    def clean_exchangeRate(self):
        exchangeRate = self.cleaned_data['exchangeRate']
        if exchangeRate <= 0:
            raise forms.ValidationError('Ingrese un tipo de cambio válido.')
        return exchangeRate
    
    def clean_idDoc(self):
        doc = self.cleaned_data['idDoc']
        if not doc:
            raise forms.ValidationError('Ingrese un documento.')
        return doc

    def __init__(self, *args, **kwargs):
        super(ConciliationMovDocForm, self).__init__(*args, **kwargs)
        self.fields['idDoc'].queryset = Documents.objects.filter(amount__gt = F('amountReconcilied'))
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class EditConciliationMovDocForm(forms.ModelForm):

    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idDoc',
            'amountReconcilied'
        ]
        widgets = {
                'idDoc': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control w-100',
                        'required':True
                    }
                ),
                'type': forms.Select(
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
            }
        
    def clean_idDoc(self):
        doc = self.cleaned_data['idDoc']
        if doc == None or doc == "None" or doc == "":
            raise forms.ValidationError('Ingrese un documento.')
        return doc
        
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        exchangeRate = self.cleaned_data['exchangeRate']
        doc = self.cleaned_data.get('idDoc',None)
        if doc == None:
            raise forms.ValidationError('Primero ingrese un documento.')
        
        movOrigin = self.cleaned_data['idMovOrigin']
        amountOrigin = BankMovements.objects.get(id = movOrigin.id)
        Doc = Documents.objects.get(id = doc.id)
        AmountDoc = Doc.amount

        accIdDoc = Conciliation.objects.SumaMontosConciliadosPorDocumentos(doc.id)
        accIdDocSum = 0 if accIdDoc["sum"] is None else accIdDoc["sum"]

        if amountReconcilied <= 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero.')
        
        diffAmountAmountReconcilied = amountOrigin.amount - amountOrigin.amountReconcilied + accIdDocSum * exchangeRate
        if amountReconcilied > diffAmountAmountReconcilied:
            raise forms.ValidationError(f'El monto máximo a conciliar es {diffAmountAmountReconcilied}')
        
        diffAmountDocaccIdDocSum = AmountDoc - accIdDocSum * exchangeRate
        if amountReconcilied > diffAmountDocaccIdDocSum:
            raise forms.ValidationError(f'El monto supera al saldo en el documento. {diffAmountDocaccIdDocSum}')
        
        return amountReconcilied


    def __init__(self, *args, **kwargs):
        super(EditConciliationMovDocForm, self).__init__(*args, **kwargs)
        self.fields['idDoc'].queryset = Documents.objects.filter(amount__gte = F('amountReconcilied'))
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class ConciliationMovMovForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idMovArrival',
            'amountReconcilied',
            'exchangeRate',
            'status'
        ]
        widgets = {
            'idMovArrival': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control w-100',
                    #'disabled': True
                }
            ),
            'idMovOrigin': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control w-100',
                    #'disabled': True
                }
            ),
            'type': forms.Select(
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
            'exchangeRate': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',
                    'type':"checkbox"
                    #'disabled': True
                }
            ),
        }
        
    def clean_idMovArrival(self):
        idMovArrival = self.cleaned_data['idMovArrival']
        if idMovArrival == None:
            raise forms.ValidationError('Ingrese un movimiento.')
        return idMovArrival
    
    def clean_amountReconcilied(self):
        amountReconcilied = self.cleaned_data['amountReconcilied']
        idMovOrigin = self.cleaned_data['idMovOrigin']
        amountOrigin = BankMovements.objects.get(id = idMovOrigin.id)
        accIdMov = Conciliation.objects.SumaMontosConciliadosPorMovimientosOr(idMovOrigin.id)
        accIdMovSum = 0 if accIdMov["sum"] is None else accIdMov["sum"]

        idMovArrival = self.cleaned_data.get("idMovArrival",None)
        if idMovArrival == None:
            raise forms.ValidationError('Primero ingrese un movimiento.')

        amountArrival = BankMovements.objects.get(id = idMovArrival.id)

        print(amountArrival.amount, amountArrival.amountReconcilied)

        if amountReconcilied <= 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero.')
        
        diff = amountOrigin.amount - accIdMovSum
        if amountReconcilied > diff:
            raise forms.ValidationError(f'Ingrese un monto menor a {diff}.')
        
        diff2 = amountArrival.amount - amountArrival.amountReconcilied
        if amountReconcilied > diff2:
            raise forms.ValidationError(f'Ingrese un monto menor a {diff}.')
        
        return amountReconcilied
    
    def clean_exchangeRate(self):
        exchangeRate = self.cleaned_data['exchangeRate']
        if exchangeRate <= 0:
            raise forms.ValidationError('Ingrese un tipo de cambio válido.')
        return exchangeRate
            
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        idAccount = BankMovements.objects.get(id = int(self.pk))
        super(ConciliationMovMovForm, self).__init__(*args, **kwargs)
        self.fields['idMovArrival'].queryset = BankMovements.objects.filter(
                                                    amount__gt = F('amountReconcilied')
                                                ).exclude(
                                                    idAccount = idAccount.idAccount.id
                                                )
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class EditConciliationMovMovForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idMovArrival',
            'amountReconcilied',
            'status',
            'exchangeRate'
        ]
        widgets = {
            'idMovArrival': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control w-100',
                    #'disabled': True
                }
            ),
            'idMovOrigin': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control w-100',
                    #'disabled': True
                }
            ),
            'type': forms.Select(
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
            'status': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',
                    'type':"checkbox"
                    #'disabled': True
                }
            ),
            'exchangeRate': forms.NumberInput(
                attrs = {
                    'class': 'input-group-field form-control',
                    #'disabled': True
                }
            ),
        }
        
    def clean_idMovArrival(self):
        idMovArrival = self.cleaned_data['idMovArrival']
        if idMovArrival == None:
            raise forms.ValidationError('Ingrese un movimiento.')
        return idMovArrival
    
    def clean_amountReconcilied(self):
        #print(self.cleaned_data)
        amountReconcilied = self.cleaned_data['amountReconcilied']
        exchangeRate = self.cleaned_data['exchangeRate']
        idOrigin = self.cleaned_data['idMovOrigin']

        idArrival = self.cleaned_data.get('idMovArrival',None)
        if idArrival == None:
            raise forms.ValidationError('Primero ingrese un movimiento.')
        
        amountOrigin = idOrigin.amount
        amountReconciliedOrigin = idOrigin.amountReconcilied
        amountReconciliedArrival = idArrival.amountReconcilied

        if amountReconcilied <= 0: # validación para depurar numeros negativos
            raise forms.ValidationError('Ingrese un monto mayor a cero.')

        diff = amountOrigin - amountReconciliedOrigin + amountReconciliedArrival * exchangeRate
        if amountReconcilied > diff: # validación par no superar el monto pendiente del movimeinto de origen
            raise forms.ValidationError(f'Ingrese un monto menor a {diff}.')
        
        diff2 = idArrival.amount - idArrival.amountReconcilied + amountReconciliedArrival * exchangeRate
        if amountReconcilied > diff2:
            raise forms.ValidationError(f'Ingrese un monto menor a {diff2}.')
        
        return amountReconcilied
            
    def __init__(self, *args, **kwargs):
        
        idMov = kwargs["instance"].idMovOrigin.id
        #self.pk = kwargs.pop("pk")
        idAccount = BankMovements.objects.get(id = idMov)
        super(EditConciliationMovMovForm, self).__init__(*args, **kwargs)
        self.fields['idMovArrival'].queryset = BankMovements.objects.filter(
                                                    amount__gte = F('amountReconcilied')
                                                ).exclude(
                                                    idAccount = idAccount.idAccount.id
                                                )
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

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
            'transactionType',
            'expenseSubCategory',
            'incomeSubCategory'
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
                        'onchange':"toggleDiv()"
                    }
                ),
                'expenseSubCategory': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                    }
                ),
                'incomeSubCategory': forms.Select(
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

            'detraction',
            'shippingGuide',
            'retention',
            'month_dec',
            'year_dec',

            'idClient',
            'typeCurrency',
            'amount',

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

                }
            ),
            'idCommission': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',

                }
            ),
            'idProject': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',

                }
            ),

            # =======================
            'expensesCategory': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',

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
        
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not amount > 0:
            raise forms.ValidationError('Ingrese un monto mayor a cero')
        return amount

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

