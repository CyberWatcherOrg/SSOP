from django.shortcuts import render

def index(request):
    return render(request, 'ssop_app/index.html')

def registration(request):
    return render(request, 'ssop_app/registration.html')

def register_user(request):
    pass


