from django import forms
from .models import *


class SMSForm(forms.ModelForm):
    class Meta:
        fields = ('numero', 'mensaje')
        model = SMSMessage
