from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {\
        'title': 'Home',
        'content': 'Главная страница магазина Siko',
        'list': ['first', 'second'],
        'dict': {'first': 1},
        'bool': False
               }

    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse('About page')