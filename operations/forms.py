from django import forms
from .models import AgentProductivity

class EmployeeForm(forms.Form):
    ACTION_CHOICES = [
        ('add', 'Add'),
        ('remove', 'Remove'),
    ]

    id = forms.IntegerField(label="Employee ID", required=True, widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Employee ID',
        }
    ))

    last_name_and_suffix = forms.CharField(label="Employee Last Name and Suffix", max_length=35, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Employee Last Name and Suffix',
        }
    ))

    first_name = forms.CharField(label="Employee First Name", max_length=25, required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Employee First Name',
        }
    ))

    most_recent_hire_date = forms.DateField(label="Most Recent Hire Date", required=False, widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control',
        }
    ))

    supervisor = forms.CharField(label="Supervisor", max_length=60, required=False,  widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Supervisor Name',
        }
    ))

    pay_rate = forms.DecimalField(label="Pay Rate", required=False,  widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Pay Rate',
        }
    ))

    action = forms.ChoiceField(choices=ACTION_CHOICES, widget=forms.RadioSelect, initial='add', required=True, )


class AgentProductivityForm(forms.ModelForm):
    class Meta:
        model = AgentProductivity
        fields = ['productivity_uploaded_file', 'calls_uploaded_file']

class AgentProductivityForm(forms.Form):
    productivity_file = forms.FileField(label="Agent Productivity Log", required=True, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Upload Agent Productivity File',
        }
    ))

    calls_file = forms.FileField(label="Agent Call Log", required=True, widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Upload Agent Call Log File',
        }
    ))
