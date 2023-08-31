from django.core.management import BaseCommand

from blogapp.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Start demo bulk actions")

        info = [
            "new",
            "top",
            "experiment",
            "smile",
        ]

        authors = [Tag(name=name) for name in info]
        result = Tag.objects.bulk_create(authors)
        for obj in result:
            print(obj)
        self.stdout.write("Done")
