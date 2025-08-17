# orders/admin.py
from django.contrib import admin
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'name', 'price', 'quantity')
    readonly_fields = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_timestamp', 'status', 'total_price')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]

    def total_price(self, obj):
        return obj.orderitem_set.total_price()
    total_price.short_description = 'Total Price'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Support').exists():
            return qs  # Support can only view
        return qs

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'name', 'price', 'quantity')
    list_filter = ('order',)
    search_fields = ('name',)