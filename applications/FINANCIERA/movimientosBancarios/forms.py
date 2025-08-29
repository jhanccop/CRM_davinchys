# django
from django import forms
from django.db.models import F

from .models import (
  #InternalTransfers,
  BankMovements,
  #Documents,
  Conciliation
)

from applications.cuentas.models import Account
from applications.FINANCIERA.documentos.models import FinancialDocuments

class BankMovementsForm(forms.ModelForm):
    class Meta:
        model = BankMovements
        fields = [
            'idAccount',
            'date',
            'description',
            'transactionType',
            'amount',
            'opNumber',
            'justification',
            'expenseSubCategory',
            'incomeSubCategory',
            'originDestination',
            'pdf_file'
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
                'transactionType': forms.Select(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
                        'onchange':"toggleDiv()"
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
                'justification': forms.TextInput(
                    attrs = {
                        'placeholder': '',
                        'class': 'input-group-field form-control',
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
                'originDestination': forms.Select(
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
        super(BankMovementsForm, self).__init__(*args, **kwargs)

        if self.request:
            self.fields['idAccount'].queryset = Account.objects.filter(idTin__id = self.request.user.company.id)

class ConciliationIntForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'amountReconcilied',
            'equivalentAmount',
            'status'
        ]
        widgets = {
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
            'equivalentAmount': forms.NumberInput(
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
    
    def clean(self):
        # recuperacion de montos
        movOrigin = self.cleaned_data['idMovOrigin']
        movOr_Amount = movOrigin.amount
        movOr_AmountCon = movOrigin.amountReconcilied
        movOr_curr = movOrigin.idAccount.currency

         # validacion DE INGRESOS NEGATIVOS O CEROS
        if self.cleaned_data['amountReconcilied'] < 0:
            raise forms.ValidationError(f'El MONTO A CONCILIAR debe ser mayor a 0.')
        if self.cleaned_data['equivalentAmount'] < 0:
            raise forms.ValidationError(f'El MONTO EQUIVALENTE A CONCILIAR debe ser mayor a 0.')

        con_Amount = self.cleaned_data['amountReconcilied']
        con_AmountEq = self.cleaned_data.get('equivalentAmount',0)
        
        # recuperacion de documento
        #idMovArrival = self.cleaned_data.get('idMovArrival',None)
        #print(idMovArrival.amount)
        #movArr_amount = idMovArrival.amount
        #movArr_AmountCon = idMovArrival.amountReconcilied
        #movArr_Curr = idMovArrival.idAccount.currency

        print(movOr_Amount,movOr_AmountCon,con_Amount,con_AmountEq,movOr_curr)
        
        # validacion respecto al moviento de origen
        if con_Amount > (movOr_Amount - movOr_AmountCon):
            diff = movOr_Amount - movOr_AmountCon
            raise forms.ValidationError(f'El monto debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del movimiento origen.')

        # verificacion de monedas
        #if movArr_Curr == movOr_curr:
        #    # validacion respecto a documento
        #    if con_Amount > (movArr_amount - movArr_AmountCon):
        #        diff = movArr_amount - movArr_AmountCon
        #        raise forms.ValidationError(f'El MONTO A CONCILIAR debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')
        #else:
        #    if con_AmountEq > (movArr_amount - movArr_AmountCon):
        #        diff = movArr_amount - movArr_AmountCon
        #        raise forms.ValidationError(f'El MONTO EQUIVALENTE debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')

    def __init__(self, *args, **kwargs):
        # Extraer el parámetro pk antes de llamar al constructor padre
        self.pk = kwargs.pop('pk', None)
        super(ConciliationIntForm, self).__init__(*args, **kwargs)
        
        # Puedes usar self.pk para personalizar el formulario
        if self.pk:
            # Ejemplo: filtrar opciones de un campo basado en el pk
            self.fields['idMovOrigin'].queryset = BankMovements.objects.filter(id=self.pk)
            self.fields['type'].choices = [
                (Conciliation.OPBANK, 'Com. Bancarias'),
                (Conciliation.IMP, 'Impuestos'),
            ]
        #return con_Amount

class ConciliationMovDocForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idDoc',
            'amountReconcilied',
            'equivalentAmount',
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
                'equivalentAmount': forms.NumberInput(
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
        
    def clean(self):
        # verificacion si hay documento
        doc = self.cleaned_data.get('idDoc',None)
        if doc == None:
            raise forms.ValidationError('Ingrese un documento.')
        
        # recuperacion de montos
        movOrigin = self.cleaned_data['idMovOrigin']
        movOr_Amount = movOrigin.amount
        movOr_AmountCon = movOrigin.amountReconcilied
        movOr_curr = movOrigin.idAccount.currency

         # validacion DE INGRESOS NEGATIVOS O CEROS
        if self.cleaned_data['amountReconcilied'] < 0:
            raise forms.ValidationError(f'El MONTO A CONCILIAR debe ser mayor a 0.')
        if self.cleaned_data['equivalentAmount'] < 0:
            raise forms.ValidationError(f'El MONTO EQUIVALENTE A CONCILIAR debe ser mayor a 0.')

        con_Amount = self.cleaned_data['amountReconcilied']
        con_AmountEq = self.cleaned_data.get('equivalentAmount',0)
        
        # recuperacion de documento
        docOr_Amount = doc.amount
        docOr_AmountCon = doc.amountReconcilied
        docOr_Curr = doc.typeCurrency
        
        # validacion respecto al moviento de origen
        if con_Amount > (movOr_Amount - movOr_AmountCon):
            diff = movOr_Amount - movOr_AmountCon
            raise forms.ValidationError(f'El monto debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del movimiento origen.')

        # verificacion de monedas
        if docOr_Curr == movOr_curr:
            # validacion respecto a documento
            if con_Amount > (docOr_Amount - docOr_AmountCon):
                diff = docOr_Amount - docOr_AmountCon
                raise forms.ValidationError(f'El MONTO A CONCILIAR debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del DOCUMENTO.')
        else:
            if con_AmountEq > (docOr_Amount - docOr_AmountCon):
                diff = docOr_Amount - docOr_AmountCon
                raise forms.ValidationError(f'El MONTO EQUIVALENTE debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del DOCUMENTO.')

        #print(movOr_Amount,movOr_AmountCon,con_Amount,con_AmountEq,docOr_Amount,docOr_Curr,movOr_curr)
        #return con_Amount

    def __init__(self, *args, **kwargs):
        self.company_id = kwargs.pop('company_id', None)
        super(ConciliationMovDocForm, self).__init__(*args, **kwargs)
        self.fields['idDoc'].queryset = FinancialDocuments.objects.filter(
            amount__gt = F('amountReconcilied'),
            idTin = self.company_id
            )
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class ConciliationMovMovForm(forms.ModelForm):
    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idMovArrival',
            'amountReconcilied',
            'equivalentAmount',
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
            'equivalentAmount': forms.NumberInput(
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
    
    def clean(self):
        # verificacion si hay movimientos
        idMovArrival = self.cleaned_data.get('idMovArrival',None)
        if idMovArrival == None:
            raise forms.ValidationError('Ingrese un movimiento de destino.')
        
        # recuperacion de montos
        movOrigin = self.cleaned_data['idMovOrigin']
        movOr_Amount = movOrigin.amount
        movOr_AmountCon = movOrigin.amountReconcilied
        movOr_curr = movOrigin.idAccount.currency

         # validacion DE INGRESOS NEGATIVOS O CEROS
        if self.cleaned_data['amountReconcilied'] < 0:
            raise forms.ValidationError(f'El MONTO A CONCILIAR debe ser mayor a 0.')
        if self.cleaned_data['equivalentAmount'] < 0:
            raise forms.ValidationError(f'El MONTO EQUIVALENTE A CONCILIAR debe ser mayor a 0.')

        con_Amount = self.cleaned_data['amountReconcilied']
        con_AmountEq = self.cleaned_data.get('equivalentAmount',0)
        
        # recuperacion de documento
        idMovArrival = self.cleaned_data.get('idMovArrival',None)
        #print(idMovArrival.amount)
        movArr_amount = idMovArrival.amount
        movArr_AmountCon = idMovArrival.amountReconcilied
        movArr_Curr = idMovArrival.idAccount.currency

        #print(movOr_Amount,movOr_AmountCon,con_Amount,con_AmountEq,movArr_amount,movArr_Curr,movOr_curr)
        
        # validacion respecto al moviento de origen
        if con_Amount > (movOr_Amount - movOr_AmountCon):
            diff = movOr_Amount - movOr_AmountCon
            raise forms.ValidationError(f'El monto debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del movimiento origen.')

        # verificacion de monedas
        if movArr_Curr == movOr_curr:
            # validacion respecto a documento
            if con_Amount > (movArr_amount - movArr_AmountCon):
                diff = movArr_amount - movArr_AmountCon
                raise forms.ValidationError(f'El MONTO A CONCILIAR debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')
        else:
            if con_AmountEq > (movArr_amount - movArr_AmountCon):
                diff = movArr_amount - movArr_AmountCon
                raise forms.ValidationError(f'El MONTO EQUIVALENTE debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')

        #return con_Amount
            
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk")
        idMovOr = BankMovements.objects.get(id = int(self.pk))
        typeT = idMovOr.transactionType
        super(ConciliationMovMovForm, self).__init__(*args, **kwargs)
        self.fields['idMovArrival'].queryset = BankMovements.objects.filter(
                                                    amount__gt = F('amountReconcilied')
                                                ).exclude(
                                                    idAccount = idMovOr.idAccount.id
                                                ).exclude(
                                                    transactionType = typeT
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
            'equivalentAmount'
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
            'equivalentAmount': forms.NumberInput(
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
    
    def clean(self):
        # verificacion si hay movimientos
        idMovArrival = self.cleaned_data.get('idMovArrival',None)
        if idMovArrival == None:
            raise forms.ValidationError('Ingrese un movimiento de destino.')
        
        # recuperacion de montos
        movOrigin = self.cleaned_data['idMovOrigin']
        movOr_Amount = movOrigin.amount
        movOr_AmountCon = movOrigin.amountReconcilied
        movOr_curr = movOrigin.idAccount.currency

         # validacion DE INGRESOS NEGATIVOS O CEROS
        if self.cleaned_data['amountReconcilied'] < 0:
            raise forms.ValidationError(f'El MONTO A CONCILIAR debe ser mayor a 0.')
        if self.cleaned_data['equivalentAmount'] < 0:
            raise forms.ValidationError(f'El MONTO EQUIVALENTE A CONCILIAR debe ser mayor a 0.')

        con_Amount = self.cleaned_data['amountReconcilied']
        con_AmountEq = self.cleaned_data.get('equivalentAmount',0)
        
        # recuperacion de documento
        idMovArrival = self.cleaned_data.get('idMovArrival',None)
        #print(idMovArrival.amount)
        movArr_amount = idMovArrival.amount
        movArr_AmountCon = idMovArrival.amountReconcilied
        movArr_Curr = idMovArrival.idAccount.currency

        #print(movOr_Amount,movOr_AmountCon,con_Amount,con_AmountEq,movArr_amount,movArr_Curr,movOr_curr)
        
        # validacion respecto al moviento de origen
        if con_Amount > (movOr_Amount - movOr_AmountCon):
            diff = movOr_Amount - movOr_AmountCon
            raise forms.ValidationError(f'El monto debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del movimiento origen.')

        # verificacion de monedas
        if movArr_Curr == movOr_curr:
            # validacion respecto a documento
            if con_Amount > (movArr_amount - movArr_AmountCon):
                diff = movArr_amount - movArr_AmountCon
                raise forms.ValidationError(f'El MONTO A CONCILIAR debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')
        else:
            if con_AmountEq > (movArr_amount - movArr_AmountCon):
                diff = movArr_amount - movArr_AmountCon
                raise forms.ValidationError(f'El MONTO EQUIVALENTE debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del MOVIENTO DESTINO.')

        #return con_Amount
    
            
    def __init__(self, *args, **kwargs):
        
        idMov = kwargs["instance"].idMovOrigin.id
        curr = kwargs["instance"].idMovOrigin.idAccount.currency
        #self.pk = kwargs.pop("pk")
        idAccount = BankMovements.objects.get(id = idMov)
        super(EditConciliationMovMovForm, self).__init__(*args, **kwargs)
        self.fields['idMovArrival'].queryset = BankMovements.objects.filter(
                                                    amount__gte = F('amountReconcilied')
                                                ).exclude(
                                                    idAccount = idAccount.idAccount.id
                                                ).exclude(
                                                    idAccount__currency = curr
                                                )
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

class EditConciliationMovDocForm(forms.ModelForm):

    class Meta:
        model = Conciliation
        fields = [
            'idMovOrigin',
            "type",
            'idDoc',
            'amountReconcilied',
            'equivalentAmount'
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
                'equivalentAmount': forms.NumberInput(
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
        
    def clean(self):
        # verificacion si hay documento
        doc = self.cleaned_data.get('idDoc',None)
        if doc == None:
            raise forms.ValidationError('Ingrese un documento.')
        
        # recuperacion de montos
        movOrigin = self.cleaned_data['idMovOrigin']
        movOr_Amount = movOrigin.amount
        movOr_AmountCon = movOrigin.amountReconcilied
        movOr_curr = movOrigin.idAccount.currency

         # validacion DE INGRESOS NEGATIVOS O CEROS
        if self.cleaned_data['amountReconcilied'] < 0:
            raise forms.ValidationError(f'El MONTO A CONCILIAR debe ser mayor a 0.')
        if self.cleaned_data['equivalentAmount'] < 0:
            raise forms.ValidationError(f'El MONTO EQUIVALENTE A CONCILIAR debe ser mayor a 0.')

        con_Amount = self.cleaned_data['amountReconcilied']
        con_AmountEq = self.cleaned_data.get('equivalentAmount',0)
        
        # recuperacion de documento
        print(doc.amount)
        docOr_Amount = doc.amount
        docOr_AmountCon = doc.amountReconcilied
        docOr_Curr = doc.typeCurrency

        print(movOr_Amount,movOr_AmountCon,con_Amount,con_AmountEq,docOr_Amount,docOr_Curr,movOr_curr)
        
        # validacion respecto al moviento de origen
        if con_Amount > (movOr_Amount - movOr_AmountCon):
            diff = movOr_Amount - movOr_AmountCon
            raise forms.ValidationError(f'El monto debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del movimiento origen.')

        # verificacion de monedas
        if docOr_Curr == movOr_curr:
            # validacion respecto a documento
            if con_Amount > (docOr_Amount - docOr_AmountCon):
                diff = docOr_Amount - docOr_AmountCon
                raise forms.ValidationError(f'El MONTO A CONCILIAR debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del DOCUMENTO.')
        else:
            if con_AmountEq > (docOr_Amount - docOr_AmountCon):
                diff = docOr_Amount - docOr_AmountCon
                raise forms.ValidationError(f'El MONTO EQUIVALENTE debe NO debe superar {diff} que es la diferencia del Monto original y el monto ya conciliado del DOCUMENTO.')

        #return con_Amount

    def __init__(self, *args, **kwargs):
        super(EditConciliationMovDocForm, self).__init__(*args, **kwargs)
        self.fields['idDoc'].queryset = FinancialDocuments.objects.filter(amount__gte = F('amountReconcilied'))
        #self.fields['idDocs'].queryset = Documents.objects.exclude(docs__isnull = False)

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

