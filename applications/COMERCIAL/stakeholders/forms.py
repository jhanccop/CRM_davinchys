from django import forms

from .models import client, supplier

class clientForm(forms.ModelForm):
    
    class Meta:
        model = client
        fields = (
            'numberIdClient',
            'tradeName',
            'brandName',
            'typeDocument',
            'location',
            'status',

            'phoneNumber',
            'webPage',
            'email',
        )
        widgets = {
            'numberIdClient': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'tradeName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'brandName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'typeDocument': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'location': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'phoneNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'webPage': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

        }
    
    def clean_numberIdClient(self):
        ruc = self.cleaned_data.get('numberIdClient')
        #if ruc and len(ruc) != 11:
        #    raise forms.ValidationError("El RUC debe tener exactamente 11 dígitos")
        if ruc and not ruc.isdigit():
            raise forms.ValidationError("El RUC debe contener solo números")
        return ruc
        
class supplierForm(forms.ModelForm):
    
    class Meta:
        model = supplier
        fields = (
            'numberIdSupplier',
            'tradeName',
            'brandName',
            'typeDocument',
            'location',
            'status',

            'phoneNumber',
            'webPage',
            'email',
        )
        widgets = {
            'numberIdSupplier': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'tradeName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'brandName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'typeDocument': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'location': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'phoneNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'webPage': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

        }
    
    def clean_numberIdSupplier(self):
        ruc = self.cleaned_data.get('numberIdSupplier')
        #if ruc and len(ruc) != 11:
        #    raise forms.ValidationError("El TIN debe tener exactamente 11 dígitos")
        if ruc and not ruc.isdigit():
            raise forms.ValidationError("El TIN debe contener solo números")
        return ruc
    
