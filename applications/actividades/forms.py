# django
from django import forms
# local
from .models import (
  Trafos,
  TrafoQuote,
  Projects,
  Commissions,
  DailyTasks,
  RestDays,
  EmailSent,
  TrafoTask,
  SuggestionBox
)
from applications.users.models import User

class ProjectsForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = [
            'projectName',
            'startDate',
            'endDate',
            'workers',
            'status',
            'description',
        ]
        widgets = {
            'projectName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'startDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'endDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'workers': forms.SelectMultiple(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'rows':3,
                    'class': 'input-group-field form-control',
                }
            ),
                        
            
        }

class CommissionsForm(forms.ModelForm):
    
    class Meta:
        model = Commissions
        fields = [
            'commissionName',
            'place',
            'startDate',
            'endDate',
            'workers',
            'status',
            'description',
        ]
        widgets = {
            'commissionName': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'place': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'startDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'endDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'workers': forms.SelectMultiple(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'status': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'rows':3,
                    'class': 'input-group-field form-control',
                }
            ),
                        
            
        }

class DailyTaskForm (forms.ModelForm):
    class Meta:
        model = DailyTasks
        fields = [
            'user',
            'date',
            'activity',
            #'is_overTime',
            'trafoOrder',
            'commissions',
            'projects',
            'assignedTasks'
        ]   
    
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'activity': forms.Textarea(
                attrs = {
                    'rows':2,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            #'is_overTime': forms.CheckboxInput(
            #    attrs = {
            #        'placeholder': '',
            #        'class': 'form-check-input',
            #        'type': 'checkbox',
            #        'onchange':"toggleDiv()"    }
            #),
            
            'trafoOrder': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'commissions': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'projects': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'assignedTasks': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class RestDaysForm (forms.ModelForm):
    class Meta:
        model = RestDays
        fields = [
            'user',
            'type',
            'motive',
            'hours',
            'isCompensated',
            'startDate',
            'endDate',
            'pdf_file'
        ]   
    
        widgets = {
            'type': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                    'onchange': "updateSelect()",
                }
            ),
            'motive': forms.Textarea(
                attrs = {
                    'rows':2,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'isCompensated': forms.CheckboxInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-check-input',
                    'type': 'checkbox'
                }
            ),
            'startDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'type':"date",
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'endDate': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'placeholder': '',
                    'type':"date",
                    'class': 'form-control datetimepicker text-center text-dark flatpickr-input',
                }
            ),
            'hours': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'type':"number",
                    'class': 'form-control',
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
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError("Archivos permitidos pdf")
            if pdf_file.size > 5*1024*1024:  # 5 MB limit
                raise forms.ValidationError("El tamaño del archivo no debe superar los 5 MB.")
        return pdf_file
    
    def clean_endDate(self):
        end_date = self.cleaned_data.get('endDate')
        start_date = self.cleaned_data.get('startDate')
        
        # Verificamos que ambas fechas estén presentes
        if end_date and start_date:
            # Comprobamos que la fecha final sea mayor que la inicial
            if end_date <= start_date:
                raise forms.ValidationError('La fecha de término debe ser posterior a la fecha de inicio.')
        
        return end_date



class QuoteTrafoForm(forms.ModelForm):
    class Meta:
        model = TrafoQuote
        fields = (
            'idQuote',
            'dateOrder',
            'deadline',

            'idClient',
            'userClient',
            
            'idAttendant',
            'description',
            'condition'
        )
        
        widgets = {
            'idQuote': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'idClient': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'userClient': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'dateOrder': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'idAttendant': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'description': forms.Textarea(
                attrs = {
                    'rows':8,
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
        }

    def __init__(self, *args, **kwargs):
        super(QuoteTrafoForm, self).__init__(*args, **kwargs)
        self.fields['idAttendant'].queryset = User.objects.filter(position = "2")

class TrafoForm(forms.ModelForm):
    class Meta:
        model = Trafos
        fields = (
            'idQuote',

            'provider',
            'quantity',

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
        )
        widgets = {
            
            'provider': forms.Select(
                attrs = {
                    'class': 'input-group-field form-control',
                }
            ),
            'quantity': forms.NumberInput(
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

class EmailSentForm(forms.ModelForm):
    class Meta:
        model = EmailSent
        fields = (
            'idQuote',
            'sender',
            'recipients',
            'subject',

            'body',
            'sendFlag'
        )
        
        widgets = {
            'idQuote': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'sender': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'recipients': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'subject': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            
            'body': forms.Textarea(
                attrs = {
                    'rows':8,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'sendFlag': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class TrafoTaskForm(forms.ModelForm):
    class Meta:
        model = TrafoTask
        fields = (
            'idTrafoQuote',
            'nameTask',
            'location',

            'start_date',
            'end_date',
            
            'progress',
            'depend',
            'is_milestone'
        )
        
        widgets = {
            'idTrafoQuote': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'nameTask': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'location': forms.TextInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs = {
                    'type': 'date',
                    'class': 'input-group-field form-control',
                }
            ),
            'progress': forms.NumberInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'depend': forms.Select(
                attrs = {
                    'rows':8,
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
            'is_milestone': forms.CheckboxInput(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

class SuggestionBoxForm(forms.ModelForm):
    class Meta:
        model = SuggestionBox
        fields = [
            'user',
            'area',
            'suggestion',
        ]
        widgets = {
            'user': forms.Select(
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
            'suggestion': forms.Textarea(
                attrs = {
                    'placeholder': '',
                    'rows':3,
                    'class': 'input-group-field form-control',
                }
            ),
                        
            
        }
