# django
from django import forms
# local
from .models import Account, ManualAccount

class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = (
            'accountName',
            'accountNumber',
            'bankName',
            'accountBalance',
            'currency',
            'description',
            'state'
        )
        widgets = {
            'accountName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'accountNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'bankName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'accountBalance': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'currency': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'state': forms.CheckboxInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class ManualAccountForm(forms.ModelForm):

    class Meta:
        model = ManualAccount
        fields = (
            'idAcount',
            'realBalance',
        )
        widgets = {
            'realBalance': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idAcount': forms.TextInput(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
        }     