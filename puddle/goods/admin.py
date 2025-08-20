# goods/admin.py
from django.contrib import admin
from django import forms
from goods.models import Products, Categories

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.current_user if hasattr(self, 'current_user') else None
        if user and user.groups.filter(name='ContentEditor').exists():
            self.fields = {k: v for k, v in self.fields.items() if k in ['description', 'image']}

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'discount', 'quantity', 'category')
    list_filter = ["discount", "quantity", "category"]
    search_fields = ('name', 'description')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

admin.site.register(Products, ProductAdmin)
admin.site.register(Categories)