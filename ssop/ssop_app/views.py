from django.shortcuts import render

def index(request):
    return render(request, 'ssop_app/index.html')
