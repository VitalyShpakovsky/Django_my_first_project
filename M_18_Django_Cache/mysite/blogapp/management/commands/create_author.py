from django.core.management import BaseCommand

from blogapp.models import Author


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Start demo bulk actions")

        info = [
            ("Max Smith", "great author"),
            ("Lev Tolstov", "good author"),
            ("Alex Miller", "OK author"),
        ]

        authors = [Author(name=name, bio=bio) for name, bio in info]
        result = Author.objects.bulk_create(authors)
        for obj in result:
            print(obj)
        self.stdout.write("Done")
