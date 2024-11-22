from django import forms
from django.contrib.auth import authenticate
#
from .models import User, Documentations

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '',
                'class': 'input-group-field form-control',
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '',
                'class': 'input-group-field form-control',
            }
        )
    )

    class Meta:
        """Meta definition for Userform."""

        model = User
        fields = (
            'email',
            'full_name',
            'last_name',
            'phoneNumber',
            'ruc',
            'dni',

            'position',
            'address',
            'gender',

            'EC_full_name',
            'EC_relationship',
            'EC_phone',
            'EC_email',
        #    'gender',
        #    'date_birth',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Apellidos ...',
                    'class': 'input-group-field form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field form-control',
                }
            ),

            'phoneNumber': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'ruc': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'position': forms.Select(
                attrs={
                    'placeholder': 'Permisos',
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'gender': forms.Select(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),

            'EC_full_name': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'EC_relationship': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'EC_phone': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'EC_email': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class LoginForm(forms.Form):
    email = forms.CharField(
        label='E-mail',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'input-group-field form-control',
                'placeholder': '',
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'input-group-field form-control',
                'placeholder': ''
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')
        
        return self.cleaned_data

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'full_name',
            'last_name',
            'email',

            'phoneNumber',
            'ruc',
            'dni',

            'position',
            'address',
            'gender',

            'EC_full_name',
            'EC_relationship',
            'EC_phone',
            'EC_email',
        )
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Nombres ...',
                    'class': 'input-group-field form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Apellidos ...',
                    'class': 'input-group-field form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Correo Electronico ...',
                    'class': 'input-group-field form-control',
                }
            ),

            'phoneNumber': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'ruc': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'position': forms.Select(
                attrs={
                    'placeholder': 'Permisos',
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'gender': forms.Select(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),

            'EC_full_name': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'EC_relationship': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            'EC_phone': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'EC_email': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
        }

class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )

class DocumentationsForm(forms.ModelForm):
    class Meta:
        model = Documentations
        fields = (
            'idUser',
            'typeDoc',
            'sumary',
            'doc_file',
            'is_multiple',
            'idDoc'
        )
        widgets = {
            'idUser': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'typeDoc': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'sumary': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'idDoc': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),

            'doc_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"doc_file",
                    'class': 'form-control text-dark',
                    'id':"id_doc_file",
                }
            ),
            'is_multiple': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
            ),
        }

    def clean_doc_file(self):
        doc_file = self.cleaned_data.get('doc_file')
        if doc_file:
            if not doc_file.name.endswith('.pdf') and not doc_file.name.endswith('.png') and not doc_file.name.endswith('.jpg') and not doc_file.name.endswith('.jpeg'):
                raise forms.ValidationError("Archivos permitidos pdf, png, jpg y jpeg.")
            if doc_file.size > 1*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 1 MB.")
        return doc_file