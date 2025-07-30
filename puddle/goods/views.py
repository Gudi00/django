from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator

from goods.models import Products

from goods.utils import q_search


# Create your views here.
def catalog(requset, category_slug=None):

    page = requset.GET.get("page", 1)
    on_sale = requset.GET.get("on_sale", None)
    order_by = requset.GET.get("order_by", None)
    query = requset.GET.get("q", None)

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))

    content = {
        "title": "Home - Каталог",
        "goods": current_page,
        "slug_url": category_slug,
    }

    return render(requset, "goods/catalog.html", content)


def product(requset, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        "product": product,
    }

    return render(requset, "goods/product.html", context)
