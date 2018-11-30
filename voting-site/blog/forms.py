from django import forms
from .models import *
from django.contrib.auth.models import User


class EntradaForm(forms.ModelForm):
    class Meta:
        fields = ("titulo", "autor", "texto", "fecha")
        model = Entrada

class LoginForm(forms.ModelForm):
    class Meta:
        fields = ('username', 'password')
        model = User