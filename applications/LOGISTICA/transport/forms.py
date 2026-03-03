from django import forms
from .models import (
    Container,
    ContainerTracking,
    File
)

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = (
            'idPetitioner',
            'containerName',
            'containerNumber',
            'year',
            'currency',
            'grossAmount',
            'taxes',
            'isOrder',
            'shortDescription',
        )
        widgets = {
            'idPetitioner': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'containerName': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'containerNumber': forms.NumberInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                    'min': '0',
                }
            ),
            'year': forms.NumberInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                    'min': '2000',
                    'max': '2100',
                }
            ),
            'currency': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'grossAmount': forms.NumberInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'id': 'id_grossAmount',
                }
            ),
            'taxes': forms.NumberInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                    'step': '0.01',
                    'min': '0',
                    'id': 'id_taxes',
                }
            ),
            'isOrder': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'shortDescription': forms.TextInput(
                attrs={
                    'placeholder': 'Descripción breve del contenedor',
                    'class': 'form-control',
                }
            ),
        }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['docType', 'name', 'date', 'description', 'con_file']
        widgets = {
            'docType': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del documento',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del documento (opcional)',
            }),
            'con_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'docType': 'Tipo de documento',
            'name': 'Nombre',
            'date': 'Fecha de emisión',
            'description': 'Descripción',
            'con_file': 'Archivo',
        }

class ContainerTrackingForm(forms.ModelForm):
    class Meta:
        model = ContainerTracking
        fields = ['area', 'status']
        widgets = {
            'area': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }
        labels = {
            'area': 'Área',
            'status': 'Estado',
        }


