# django
from django import forms
# local
from .models import Workers

class WorkersForm(forms.ModelForm):
    
    class Meta:
        model = Workers
        fields = (
            'full_name',
            'last_name',
            'email',
            'phoneNumber',
            'area',
            'gender',
            'condition',
            'currency',
            'salary',
            'date_entry',
            'date_termination',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'last_name': forms.TextInput(
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
            'phoneNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'area': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'gender': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'condition': forms.Select(
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
            'salary': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'date_entry': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'date_termination': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            
        }

        