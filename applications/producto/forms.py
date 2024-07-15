# django
from django import forms
# local
from .models import Transformer

class TransformerForm(forms.ModelForm):
    
    class Meta:
        model = Transformer
        fields = (
            'barcode',

            'provider',
            'model_name',

            'KVA',
            'HVTAP',
            'KTapHV',
            'FIXHV',

            'LV',
            'HZ',
            'TYPE',
            'MOUNTING',

            'COOLING',
            'WINDING',
            'INSULAT',
            'CONNECTION',

            'STANDARD',
            'description',
        )
        widgets = {
            'barcode': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'provider': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'model_name': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'KVA': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'HVTAP': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'KTapHV': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'FIXHV': forms.Select(
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
            'TYPE': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'MOUNTING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'COOLING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'WINDING': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'INSULAT': forms.Select(
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
            'description': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'rows': '3',
                    'class': 'input-group-field form-control',
                }
            )
        }