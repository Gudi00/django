
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
        try:
            product_ct = ContentType.objects.get_for_model(Products)
            category_ct = ContentType.objects.get_for_model(Categories)
            order_ct = ContentType.objects.get_for_model(Order)
            order_item_ct = ContentType.objects.get_for_model(OrderItem)
            cart_ct = ContentType.objects.get_for_model(Cart)
            user_ct = ContentType.objects.get_for_model(User)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting content types: {str(e)}"))
            return

        # Ensure permissions exist
        permissions = {
            'view_product': Permission.objects.get_or_create(
                content_type=product_ct, codename='view_product', defaults={'name': 'Can view product'}
            )[0],
            'add_product': Permission.objects.get_or_create(
                content_type=product_ct, codename='add_product', defaults={'name': 'Can add product'}
            )[0],
            'change_product': Permission.objects.get_or_create(
                content_type=product_ct, codename='change_product', defaults={'name': 'Can change product'}
            )[0],
            'view_category': Permission.objects.get_or_create(
                content_type=category_ct, codename='view_category', defaults={'name': 'Can view category'}
            )[0],
            'add_category': Permission.objects.get_or_create(
                content_type=category_ct, codename='add_category', defaults={'name': 'Can add category'}
            )[0],
            'change_category': Permission.objects.get_or_create(
                content_type=category_ct, codename='change_category', defaults={'name': 'Can change category'}
            )[0],
            'add_order': Permission.objects.get_or_create(
                content_type=order_ct, codename='add_order', defaults={'name': 'Can add order'}
            )[0],
            'view_order': Permission.objects.get_or_create(
                content_type=order_ct, codename='view_order', defaults={'name': 'Can view order'}
            )[0],
            'change_order': Permission.objects.get_or_create(
                content_type=order_ct, codename='change_order', defaults={'name': 'Can change order'}
            )[0],
            'add_orderitem': Permission.objects.get_or_create(
                content_type=order_item_ct, codename='add_orderitem', defaults={'name': 'Can add order item'}
            )[0],
            'view_orderitem': Permission.objects.get_or_create(
                content_type=order_item_ct, codename='view_orderitem', defaults={'name': 'Can view order item'}
            )[0],
            'change_orderitem': Permission.objects.get_or_create(
                content_type=order_item_ct, codename='change_orderitem', defaults={'name': 'Can change order item'}
            )[0],
            'add_cart': Permission.objects.get_or_create(
                content_type=cart_ct, codename='add_cart', defaults={'name': 'Can add cart'}
            )[0],
            'view_cart': Permission.objects.get_or_create(
                content_type=cart_ct, codename='view_cart', defaults={'name': 'Can view cart'}
            )[0],
            'view_user': Permission.objects.get_or_create(
                content_type=user_ct, codename='view_user', defaults={'name': 'Can view user'}
            )[0],
        }

        # 1. Client Group
        client_group, _ = Group.objects.get_or_create(name='Client')
        client_permissions = [
            permissions['view_product'],
            permissions['view_category'],
            permissions['add_order'],
            permissions['view_order'],
            permissions['add_orderitem'],
            permissions['view_orderitem'],
            permissions['add_cart'],
            permissions['view_cart'],
        ]
        client_group.permissions.set(client_permissions)
        self.stdout.write(self.style.SUCCESS('Client group created with permissions'))

        # 2. Manager Group
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        manager_permissions = [
            permissions['add_product'],
            permissions['change_product'],
            permissions['view_product'],
            permissions['add_category'],
            permissions['change_category'],
            permissions['view_category'],
            permissions['add_order'],
            permissions['change_order'],
            permissions['view_order'],
            permissions['add_orderitem'],
            permissions['change_orderitem'],
            permissions['view_orderitem'],
        ]
        manager_group.permissions.set(manager_permissions)
        self.stdout.write(self.style.SUCCESS('Manager group created with permissions'))

        # 3. Content Editor Group
        content_editor_group, _ = Group.objects.get_or_create(name='ContentEditor')
        content_editor_permissions = [
            permissions['change_product'],
            permissions['view_product'],
            permissions['view_category'],
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
            permissions['view_order'],
            permissions['view_orderitem'],
            permissions['view_user'],
        ]
        support_group.permissions.set(support_permissions)
        self.stdout.write(self.style.SUCCESS('Support group created with permissions'))
