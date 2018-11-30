from django.shortcuts import render

from ssop_app.forms import UserForm, CompanyForm


def index(request):
    return render(request, 'ssop_app/index.html')

def user_registration(request):
    form = UserForm(request.POST)
    context = {'form' : form}
    return render(request, 'ssop_app/user_registration.html', context)

def register_user(request):
    pass

def company_registration(request):
    form = CompanyForm(request.POST)
    context = {'form' : form}
    return render(request, 'ssop_app/company_registration.html', context)

def register_company(request):
    pass


