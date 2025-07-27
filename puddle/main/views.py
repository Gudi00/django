from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {\
        'title': 'Home - Главная',
        'content': 'Главная страница магазина Siko',
        'list': ['first', 'second'],
        'dict': {'first': 1},
        'bool': False
               }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст про магазин и его крутость.'
        
               }

    return render(request, 'main/about.html', context)
