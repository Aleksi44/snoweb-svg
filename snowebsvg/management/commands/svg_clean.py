from django.core.management.base import BaseCommand
from snowebsvg.models import Collection


class Command(BaseCommand):

    def handle(self, *args, **options):
        Collection.objects.all().delete()
