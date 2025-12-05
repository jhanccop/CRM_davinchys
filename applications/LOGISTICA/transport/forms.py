from django import forms
from .models import (
    Container,
    ContainerTracking,
)

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = (

            # OCULTO
            'idPetitioner',
            
            # 
            'containerName',
            'currency',
            'grossAmount',
            'taxes',
            'isOrder',
            'shortDescription',
            #'item_container',
        )
        widgets = {
            'idPetitioner': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'currency': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'grossAmount': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'step': '0.01',
                    'min': '0'
                }
            ),
            'taxes': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'step': '0.01',
                    'min': '0'
                }
            ),
            'item_container': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'shortDescription': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'containerName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'isOrder': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
            ),
            
            #'fat_file': forms.ClearableFileInput(
            #    attrs = {
            #        'type':"file",
            #        'name':"fat_file",
            #        'class': 'form-control text-dark',
            #        'id':"id_fat_file",
            #        'accept':".pdf,.jpg,.jpeg,.png"
            #    }
            #),
        }
    
    #def clean_fat_file(self):
    #    fat_file = self.cleaned_data.get('fat_file')
    #    if fat_file:
    #        if not fat_file.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
    #            raise forms.ValidationError("Archivos permitidos .pdf, .jpg, .jpeg, .png")
    #        if fat_file.size > 5*1024*1024:  # 5 MB limit
    #            raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
    #    return fat_file

