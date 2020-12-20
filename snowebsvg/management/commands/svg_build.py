import os
from django.core.management.base import BaseCommand
from snowebsvg.models import Collection


class Command(BaseCommand):

    def handle(self, *args, **options):
        instance = Collection()
        for collection_name in os.listdir(instance.root_directory):
            # We don't build private files
            if not collection_name.startswith('_'):
                collection, _ = Collection.objects.get_or_create(key=collection_name)
                collection.build()
