# django
from django import forms
# local
from .models import (
  Trafos,
  TrafoQuote,
  Projects,
  Commissions,
  DailyTasks,
  EmailSent
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
            'is_overTime',
            'startTime',
            'endTime',
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
            'is_overTime': forms.CheckboxInput(
                attrs = {
                    'placeholder': '',
                    'class': 'form-check-input',
                    'type': 'checkbox',
                    'onchange':"toggleDiv()"
                }
            ),
            'startTime': forms.TimeInput(
                attrs = {
                    'placeholder': '',
                    'type':"time",
                    'class': 'form-control',
                }
            ),
            'endTime': forms.TimeInput(
                attrs = {
                    'placeholder': '',
                    'type':"time",
                    'class': 'form-control',
                }
            ),
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

