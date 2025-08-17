# notifications/admin.py
from django.contrib import admin
from django.db.models import Count
from goods.models import Products
from orders.models import Order, OrderItem

# @admin.register(Products)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'discount', 'quantity', 'orders_count')

#     def orders_count(self, obj):
#         return OrderItem.objects.filter(product=obj).count()
#     orders_count.short_description = 'Number of Orders'

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'created_timestamp', 'status', 'total_price')

#     def total_price(self, obj):
#         return obj.orderitem_set.total_price()
#     total_price.short_description = 'Total Price'