from django.shortcuts import render, reverse, HttpResponseRedirect
from .forms import *
from prueba_envio_sms.settings import ACCOUNT_SID, AUTH_TOKEN
from twilio.rest import Client

# Create your views here.


# Renderiza la index
def render_index(request):
    return render(request, "envio_sms/index.html")


# Envía un mensaje por SMS
def enviar_mensaje(request):
    if request.method == "POST":
        # Inicializa el formulario y comprueba si este es valido
        form = SMSForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtiene los datos del formulario
            numero = form.cleaned_data["numero"]
            mensaje = form.cleaned_data["mensaje"]
            #Realiza una operación de envio de SMS, utilizando el cliente de twilo,
            #en la demo solo se podran enviar SMS de números verificados
            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(to="+34" + numero, from_="+34931071691", body=mensaje)

    return HttpResponseRedirect(reverse("index"))
