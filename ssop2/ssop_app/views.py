import os
import random

import requests
from django.shortcuts import render, redirect
from twilio.rest import Client

from ssop.settings import ACCOUNT_SID, AUTH_TOKEN


def enter_pin(request):
    #token = request.GET.get('token')

    code = ''
    phone_number = request.user.last_name;
    for i in range(0, 6):
        code += str(random.randint(0, 9))
    user = request.user
    user.first_name = code
    user.save()
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(to=phone_number,
                           from_='+34' + str(os.environ.get("PROVIDER_PHONE")),
                           body=code)
    context = {'code': code}

    #context = {'token' : token}
    return render(request, 'ssop_app/enter_pin.html', context)

def send_pin(request):
    token = request.GET.get('token')
    print(token)
    pin = request.GET.get('pin')
    # TODO Check PIN in database
    # TODO If the PIN fails, we will remove token from database

    # ws = requests.get('http://localhost:8000/userinfo/?access_token=' + token)

    return redirect('http://localhost:8001/?token=' + token)

def validate(request):

    if request.method == "POST":
        token = request.POST.get('token')
        pin = request.POST.get('pin')

        # TODO compare with the PIN in the database
        if request.user.first_name == pin:
            return redirect('http://localhost:8001/?token=' + token)

    return redirect('enter_pin')
