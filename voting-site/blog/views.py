from django.shortcuts import render

def render_index(request):
    token = request.GET.get('token')
    print(token)
    context = {'token' : token}
    return render(request, "blog/index.html", context)
