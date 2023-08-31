from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """
    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_info = [('Laptop', 'Made in China', 1999),
                         ('Netbook', 'Made in China', 2999),
                         ('Smartphone', 'Made in China', 1000),
                         ]
        for product_info in products_info:
            product, created = Product.objects.get_or_create(name=product_info[0], description=product_info[1],
                                                             price=product_info[2])
            self.stdout.write(f"Created product {product_info[0]}")

        self.stdout.write(self.style.SUCCESS("Products created"))
