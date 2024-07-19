# django
from django import forms
# local
from .models import TrafoQuote, Projects, Commissions, DailyTasks

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
            'type',
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
            'type': forms.Select(
                attrs = {
                    'placeholder': '',
                    'class': 'input-group-field form-control',
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
            'idClient',
            'userClient',
            'dateOrder',
            'deadline',
            'idAttendant',
            'description'
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
                    'placeholder': '',
                    'class': 'input-group-field form-control',
                }
            ),
        }

