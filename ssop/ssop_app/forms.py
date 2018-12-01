from django import forms

from ssop_app.models import User, Company, SMSMessage


class UserForm(forms.ModelForm):
    class Meta:
        fields = ('dni', 'name', 'surname', 'address', 'city', 'province', 'phone', 'email')
        model = User

class CompanyForm(forms.ModelForm):
    class Meta:
        fields = ('cif', 'comercial_name', 'official_name', 'address', 'city', 'province',
                  'phone', 'email', 'contact_name', 'contact_surname')
        model = Company


class SMSForm(forms.ModelForm):
    class Meta:
        fields = ('number',)
        model = SMSMessage
