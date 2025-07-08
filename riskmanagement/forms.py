from django import forms 
from .models import Audit


class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit
        fields = ['audit_type', 'client', 'start_date', 'due_date',]

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


