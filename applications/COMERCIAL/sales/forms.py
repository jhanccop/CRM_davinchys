from django import forms

from django.core.exceptions import ValidationError

from .models import (
    Incomes,
    quotes,
    IntQuotes,
    Items,
    ItemTracking,
    ItemImage,
    Trafo,
    WorkOrder
)

from django.forms import inlineformset_factory
from applications.users.models import User
from applications.cuentas.models import Tin
from applications.COMERCIAL.stakeholders.models import supplier

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
            'idClient',

            'dateOrder',
            'deadline',

            'currency',
            'initialAmount',
            'amount',
            'payMethod',
            
            'shortDescription',
            'isPO',
            'poNumber',
            'pdf_file'
        )
        
        widgets = {
            'idTinReceiving': forms.Select(
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
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
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
            'poNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
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
            'poNumber':'Número de PO'
        }

    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if pdf_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return pdf_file
    

    #def __init__(self, *args, **kwargs):
    #    super(quotesForm, self).__init__(*args, **kwargs)
    #    self.fields['idAttendant'].queryset = User.objects.filter(position = "2")

class trafoForm(forms.ModelForm):
    class Meta:
        model = Trafo
        fields = (

            # COMERCIAL
            'drawing_file',

            # TIPO
            'PHASE',
            'COOLING',
            'MOUNTING',

            # CARACTERISTICAS TECNICAS
            'KVA',
            'HV',
            'LV',
            'HZ',
            'WINDING',
            'CONNECTION',
            'STANDARD',
            
        )
        widgets = {
            'PHASE': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'COOLING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'MOUNTING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'KVA': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'HV': forms.Select(
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
            'WINDING': forms.Select(
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
            
            'drawing_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"drawing_file",
                    'class': 'form-control text-dark',
                    'id':"id_drawing_file",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
        }
    
    def clean_drawing_file(self):
        drawing_file = self.cleaned_data.get('drawing_file')
        if drawing_file:
            if not drawing_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if drawing_file.size > 20*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 8 MB.")
        return drawing_file

class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = (

            # COMERCIAL
            'idTrafoQuote',
            'idTrafo',
            'idContainer',
            'seq',
            'unitCost',
            'fat_file',
            'plate_file',
            'plateB_file',

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
            'idContainer': forms.Select(
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
            
            'fat_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"fat_file",
                    'class': 'form-control text-dark',
                    'id':"id_fat_file",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
            'plate_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"drawing_file",
                    'class': 'form-control text-dark',
                    'id':"id_drawing_file",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
            'plateB_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"drawing_file",
                    'class': 'form-control text-dark',
                    'id':"id_drawing_file",
                    'accept':".pdf,.jpg,.jpeg,.png"
                }
            ),
        }
    
    def clean_fat_file(self):
        fat_file = self.cleaned_data.get('fat_file')
        if fat_file:
            if not fat_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if fat_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return fat_file
    
    def clean_plate_file(self):
        plate_file = self.cleaned_data.get('plate_file')
        if plate_file:
            if not plate_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if plate_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return plate_file
    
    def clean_plateB_file(self):
        plateB_file = self.cleaned_data.get('plateB_file')
        if plateB_file:
            if not plateB_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
            if plateB_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return plateB_file

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
            'statusPlate': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image', 'order', 'is_main', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la imagen (opcional)'
            })
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Validación adicional si es necesario
        return cleaned_data

class MultipleItemImageForm(forms.Form):
    """Formulario para subir múltiples imágenes a la vez"""
    images = MultipleFileField(
        label='Seleccionar imágenes (máximo 5)',
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, item=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.item = item
    
    def clean_images(self):
        images = self.files.getlist('images')
        
        if self.item:
            current_count = ItemImage.objects.filter(item=self.item).count()
            if current_count + len(images) > 5:
                raise ValidationError(
                    f'Solo puedes tener máximo 5 imágenes. '
                    f'Actualmente tienes {current_count} imágenes.'
                )
        
        if len(images) > 5:
            raise ValidationError('No puedes subir más de 5 imágenes a la vez.')
        
        # Validar tamaño y tipo de archivo
        for image in images:
            if image.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError(
                    f'El archivo {image.name} es muy grande. '
                    'Tamaño máximo: 5MB'
                )
            
            if not image.content_type.startswith('image/'):
                raise ValidationError(
                    f'El archivo {image.name} no es una imagen válida.'
                )
        
        return images

# =========================== INT QUOTES FORM ===========================

class IntQuoteForm(forms.ModelForm):
    """Formulario para crear/editar cotizaciones internas (IntQuotes)"""

    class Meta:
        model = IntQuotes
        fields = [
            'idTinReceiving',
            'currency',
            'dateOrder',
            'deadline',
            'payMethod',
            'poNumber',
        ]
        widgets = {
            'idTinReceiving': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione compañía',
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control',
            }),
            'dateOrder': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'payMethod': forms.Select(attrs={
                'class': 'form-control',
            }),
            'poNumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número PO',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.quote = kwargs.pop('quote', None)
        super().__init__(*args, **kwargs)
        # Mostrar todas las compañías TIN disponibles
        self.fields['idTinReceiving'].queryset = Tin.objects.all()
        self.fields['idTinReceiving'].label = 'Compañía Subsidiaria'
        self.fields['idTinReceiving'].empty_label = '-- Seleccionar compañía --'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.quote:
            instance.idClient = self.quote.idClient
        if commit:
            instance.save()
        return instance
    
class IntQuoteEditForm(forms.ModelForm):
    """Formulario para editar cotizaciones internas existentes"""

    class Meta:
        model = IntQuotes
        fields = [
            'idClient',
            'idTinReceiving',
            'currency',
            'dateOrder',
            'deadline',
            'payMethod',
            'poNumber',
            'pdf_file'
        ]
        widgets = {
            'idClient': forms.Select(attrs={'class': 'form-control'}),
            'idTinReceiving': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'dateOrder': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'payMethod': forms.Select(attrs={'class': 'form-control'}),
            'poNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PO-0001'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idTinReceiving'].queryset = Tin.objects.all()
        self.fields['idTinReceiving'].label = 'Compania Subsidiaria'
        self.fields['idTinReceiving'].empty_label = '-- Seleccionar compania --'
        self.fields['idClient'].label = 'Cliente'
        self.fields['idClient'].empty_label = '-- Seleccionar cliente --'

# =========================== WorkOrders FORM ===========================
class WorkOrderForm(forms.ModelForm):
    """Formulario para crear/editar órdenes de trabajo (WorkOrder)"""

    class Meta:
        model = WorkOrder
        fields = [
            'idSupplier',
            'idTinReceiving',
            'currency',
            'dateOrder',
            'deadline',
            'payMethod',
            'woNumber',
        ]
        widgets = {
            'idSupplier': forms.Select(attrs={'class': 'form-control'}),
            'idTinReceiving': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'dateOrder': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'payMethod': forms.Select(attrs={'class': 'form-control'}),
            'woNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WO-0001'}),
        }

    def __init__(self, *args, **kwargs):
        self.int_quote = kwargs.pop('int_quote', None)
        super().__init__(*args, **kwargs)
        self.fields['idSupplier'].queryset = supplier.objects.all()
        self.fields['idSupplier'].label = 'Proveedor'
        self.fields['idSupplier'].empty_label = '-- Seleccionar proveedor --'
        self.fields['idTinReceiving'].queryset = Tin.objects.all()
        self.fields['idTinReceiving'].label = 'Compañía Ejecutora'
        self.fields['idTinReceiving'].empty_label = '-- Seleccionar compañía --'

        # Pre-llenar compañía ejecutora desde la IntQuote
        if self.int_quote and self.int_quote.idTinReceiving:
            self.fields['idTinReceiving'].initial = self.int_quote.idTinReceiving.id

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class WorkOrderEditForm(forms.ModelForm):
    """Formulario para editar ordenes de trabajo existentes"""

    class Meta:
        model = WorkOrder
        fields = [
            'idSupplier',
            'idTinReceiving',
            'currency',
            'dateOrder',
            'deadline',
            'payMethod',
            'woNumber',
            'pdf_file'
        ]
        widgets = {
            'idSupplier': forms.Select(attrs={'class': 'form-control'}),
            'idTinReceiving': forms.Select(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'dateOrder': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            #'dateOrder': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            #'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payMethod': forms.Select(attrs={'class': 'form-control'}),
            'woNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WO-0001'}),
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
        super().__init__(*args, **kwargs)
        self.fields['idSupplier'].queryset = supplier.objects.all()
        self.fields['idSupplier'].label = 'Proveedor'
        self.fields['idSupplier'].empty_label = '-- Seleccionar proveedor --'
        self.fields['idTinReceiving'].queryset = Tin.objects.all()
        self.fields['idTinReceiving'].label = 'Compania Ejecutora'
        self.fields['idTinReceiving'].empty_label = '-- Seleccionar compania --'
