
# notifications/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from goods.models import Products, Categories
from orders.models import Order, OrderItem
from carts.models import Cart
from users.models import User

class Command(BaseCommand):
    help = 'Create user groups with specific permissions for the furniture sales project'

    def handle(self, *args, **kwargs):
        # Get content types for models
        product_ct = ContentType.objects.get_for_model(Products)
        category_ct = ContentType.objects.get_for_model(Categories)
        order_ct = ContentType.objects.get_for_model(Order)
        order_item_ct = ContentType.objects.get_for_model(OrderItem)
        cart_ct = ContentType.objects.get_for_model(Cart)
        user_ct = ContentType.objects.get_for_model(User)

        # 1. Client Group
        client_group, _ = Group.objects.get_or_create(name='Client')
        client_permissions = [
            Permission.objects.get(content_type=product_ct, codename='view_product'),
            Permission.objects.get(content_type=category_ct, codename='view_category'),
            Permission.objects.get(content_type=order_ct, codename='add_order'),
            Permission.objects.get(content_type=order_ct, codename='view_order'),
            Permission.objects.get(content_type=order_item_ct, codename='add_orderitem'),
            Permission.objects.get(content_type=order_item_ct, codename='view_orderitem'),
            Permission.objects.get(content_type=cart_ct, codename='add_cart'),
            Permission.objects.get(content_type=cart_ct, codename='view_cart'),
        ]
        client_group.permissions.set(client_permissions)
        self.stdout.write(self.style.SUCCESS('Client group created with permissions'))

        # 2. Manager Group
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        manager_permissions = [
            Permission.objects.get(content_type=product_ct, codename='add_product'),
            Permission.objects.get(content_type=product_ct, codename='change_product'),
            Permission.objects.get(content_type=product_ct, codename='view_product'),
            Permission.objects.get(content_type=category_ct, codename='add_category'),
            Permission.objects.get(content_type=category_ct, codename='change_category'),
            Permission.objects.get(content_type=category_ct, codename='view_category'),
            Permission.objects.get(content_type=order_ct, codename='add_order'),
            Permission.objects.get(content_type=order_ct, codename='change_order'),
            Permission.objects.get(content_type=order_ct, codename='view_order'),
            Permission.objects.get(content_type=order_item_ct, codename='add_orderitem'),
            Permission.objects.get(content_type=order_item_ct, codename='change_orderitem'),
            Permission.objects.get(content_type=order_item_ct, codename='view_orderitem'),
        ]
        manager_group.permissions.set(manager_permissions)
        self.stdout.write(self.style.SUCCESS('Manager group created with permissions'))

        # 3. Content Editor Group
        content_editor_group, _ = Group.objects.get_or_create(name='ContentEditor')
        content_editor_permissions = [
            Permission.objects.get(content_type=product_ct, codename='change_product'),
            Permission.objects.get(content_type=product_ct, codename='view_product'),
            Permission.objects.get(content_type=category_ct, codename='view_category'),
        ]
        content_editor_group.permissions.set(content_editor_permissions)
        self.stdout.write(self.style.SUCCESS('Content Editor group created with permissions'))

        # 4. Administrator Group
        admin_group, _ = Group.objects.get_or_create(name='Administrator')
        admin_group.permissions.set(Permission.objects.all())  # Full access
        self.stdout.write(self.style.SUCCESS('Administrator group created with full permissions'))

        # 5. Support Group
        support_group, _ = Group.objects.get_or_create(name='Support')
        support_permissions = [
            Permission.objects.get(content_type=order_ct, codename='view_order'),
            Permission.objects.get(content_type=order_item_ct, codename='view_orderitem'),
            Permission.objects.get(content_type=user_ct, codename='view_user'),
        ]
        support_group.permissions.set(support_permissions)
        self.stdout.write(self.style.SUCCESS('Support group created with permissions'))
