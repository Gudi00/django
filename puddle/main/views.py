from unicodedata import category
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from goods.models import Categories

# Create your views here.
def index(request):

    categories = Categories.objects.all()
    context = {
        'title': 'Home - Главная',
        'content': 'Главная страница магазина Siko',
        'categories': categories
               }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст про магазин и его крутость.'
        
               }

    return render(request, 'main/about.html', context)
