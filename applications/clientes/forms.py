# django
from django import forms
# local
from .models import Cliente

class ClientForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = (
            'ruc',
            'tradeName',
            'brandName',
            'typeClient',
            'channel',
            'languageContract',
            'locationClient',

            'phoneNumber',
            'contact',
            'webPage',
            'email',

            'legalJurisdiction',
            'internationalBilling',
            'electronicSignature'
        )
        widgets = {
            'ruc': forms.TextInput(
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
            'typeClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'channel': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'languageContract': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'locationClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'legalJurisdiction': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',
                    'type': 'checkbox'
                }
            ),
            'internationalBilling': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',
                    'type': 'checkbox'
                }
            ),
            'electronicSignature': forms.CheckboxInput(
                attrs = {
                    'class': 'form-check-input',
                    'type': 'checkbox'
                }
            ),
           
            'phoneNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'contact': forms.Select(
                attrs = {
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
    
    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if ruc and len(ruc) != 11:
            raise forms.ValidationError("El RUC debe tener exactamente 11 dígitos")
        if ruc and not ruc.isdigit():
            raise forms.ValidationError("El RUC debe contener solo números")
        return ruc

