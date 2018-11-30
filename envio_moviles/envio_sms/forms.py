from django import forms
from .models import *

class SMSForm(forms.ModelForm):
    class Meta:
        fields = ('number', 'message')
        model = SMSMessage
