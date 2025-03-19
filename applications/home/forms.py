from django import forms

from .models import (
  ContainerTracking,
)

class TrackingForm(forms.ModelForm):
    class Meta:
        model = ContainerTracking
        fields = [
            'trackingNumber',
            'pdf_file',
            'status',
        ]
        widgets = {
            'trackingNumber': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.Select(
                attrs = {
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
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf') and not pdf_file.name.endswith('.png') and not pdf_file.name.endswith('.jpg') and not pdf_file.name.endswith('.jpeg'):
                raise forms.ValidationError("Archivos permitidos pdf, png, jpg y jpeg.")
            if pdf_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return pdf_file
