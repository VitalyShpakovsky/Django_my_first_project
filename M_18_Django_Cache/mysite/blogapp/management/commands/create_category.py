from django.core.management import BaseCommand

from blogapp.models import Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Start demo bulk actions")

        info = [
            "News",
            "Technologies",
            "Humor",
            "History",
        ]

        authors = [Category(name=name) for name in info]
        result = Category.objects.bulk_create(authors)
        for obj in result:
            print(obj)
        self.stdout.write("Done")