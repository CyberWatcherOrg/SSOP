from django.shortcuts import render, reverse, HttpResponseRedirect
from .forms import *
from prueba_envio_sms.settings import ACCOUNT_SID, AUTH_TOKEN
from twilio.rest import Client

def render_index(request):
    return render(request, "envio_sms/index.html")

# Send a message via SMS
def send_sms(request):
    if request.method == "POST":
        form = SMSForm(request.POST, request.FILES)
        if form.is_valid():
            number = form.cleaned_data["number"]
            message = form.cleaned_data["message"]
            # Send a message using twilo library 
            # You only can send message to verified numbers
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(to="+34" + number, from_="+34931071691", body=message)

    return HttpResponseRedirect(reverse("index"))
