from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order


class Command(BaseCommand):
    """
    Creates order
    """
    def handle(self, *args, **options):
        self.stdout.write("Create order")
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address="st. Pobeda, h. 45 r. 9",
            promocode="VICTORY",
            user=user,
        )
        self.stdout.write(f"Created order {order}")
