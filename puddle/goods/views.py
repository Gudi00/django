from django.shortcuts import render

from goods.models import Products


# Create your views here.
def catalog(requset):

    goods = Products.objects.all()
    
    content = {
        "title": "Home - Каталог",
        "goods": goods
    }

    return render(requset, "goods/catalog.html", content)


def product(requset):
    return render(requset, "goods/product.html")
