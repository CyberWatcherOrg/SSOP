from django.shortcuts import render, reverse, HttpResponseRedirect
from ssop.settings import ACCOUNT_SID, AUTH_TOKEN
from ssop_app.forms import UserForm, CompanyForm, SMSForm
from twilio.rest import Client
import random


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


# Sends an sms to the specified number with a 6 digit random code
# and returns the code so we can work with it later on
def send_sms(request):
    if request.method == "POST":
        # Form is initialized and it is check if it's valid
        form = SMSForm(request.POST, request.FILES)
        if form.is_valid():
            code = ''
            number = form.cleaned_data["number"]
            for i in range(0, 6):
                code += str(random.randint(0, 9))
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(to='+34' + number, from_='+34931071691', body=code)
            context = {'code': code}

            return render(request, "ssop_app/index.html", context)

    return render(request, "ssop_app/index.html")
