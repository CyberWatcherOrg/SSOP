import random

import requests
from django.shortcuts import render, redirect
from twilio.rest import Client

from ssop.settings import ACCOUNT_SID, AUTH_TOKEN


def enter_pin(request):
    #token = request.GET.get('token')

    code = ''
    for i in range(0, 6):
        code += str(random.randint(0, 9))
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(to='+34615839042',from_='+34931071691', body=code)
    context = {'code': code, 'number': "+34615839042"}

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
        # if(code == received_cod):
            #The user is the actual one
        return redirect('http://localhost:8001/?token=' + token)

    return redirect('http://localhost:8001')
