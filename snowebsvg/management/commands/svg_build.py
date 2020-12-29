import os
from django.core.management.base import BaseCommand
from snowebsvg.models import Collection
from snowebsvg import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        for collection_name in os.listdir(settings.dir_collection()):
            collection, _ = Collection.objects.get_or_create(key=collection_name)
            collection.build()
