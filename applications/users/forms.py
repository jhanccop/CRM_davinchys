from django import forms
from django.contrib.auth import authenticate
#
from .models import User

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
            'position',
            'last_name',
        #    'gender',
        #    'date_birth',
        )
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'value': '@mail',
                    #'disabled': True
                }
            ),
            'full_name': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'position': forms.Select(
                attrs={
                    'placeholder': '',
                    'class': 'form-control',
                }
            ),
            
            'is_active': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
            ),

            #'position': forms.Select(
            #    attrs={
            #        'placeholder': 'position ...',
            #        'class': 'input-group-field',
            #    }
            #),
            #'date_birth': forms.DateInput(
            #    format='%Y-%m-%d',
            #    attrs={
            #        'type': 'date',
            #        'class': 'input-group-field',
            #    },
            #),
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

            #'gender',
            #'date_birth',

            'email',
            'position',

            'cv_file',
            #'condition',

            #'date_entry',
            #'date_termination',

            #'salary',
            #'currency',
            
            'is_active',
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
            'position': forms.Select(
                attrs={
                    'placeholder': 'Permisos',
                    'class': 'form-control',
                }
            ),
            'cv_file': forms.ClearableFileInput(
                attrs = {
                    'type':"file",
                    'name':"pdf_file",
                    'class': 'form-control text-dark',
                    'id':"id_pdf_file",
                }
            ),
            
            'is_active': forms.CheckboxInput(
                attrs={
                    'type':'checkbox',
                    'class': 'form-check-input',
                },
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