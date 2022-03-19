import logging
from decouple import config
from time import time, sleep
import psycopg2
import requests
from django.core import management
from django.core.cache import cache
from django.conf import settings
from snowebsvg import settings as snowebsvg_settings

check_timeout = 30
check_interval = 1
interval_unit = "second" if check_interval == 1 else "seconds"
start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
assert check_timeout > 0
assert check_interval < check_timeout


def pg_is_ready(host, user, password, dbname, port):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info(f"Postgres isn't ready. Waiting for {check_interval} {interval_unit}...")
            sleep(check_interval)

    logger.error(f"We could not connect to Postgres within {check_timeout} seconds.")
    return False


class Command(management.base.BaseCommand):

    def handle(self, *args, **options):
        # Wait for postgresql
        if not settings.DEBUG:
            pg_is_ready(
                'snowebsvg_db',
                config('DATABASE_USER', default='postgres'),
                config('DATABASE_PASSWORD', default='postgres'),
                config('DATABASE_NAME', default='postgres'),
                '5432'
            )
            if settings.AWS_SECRET_ACCESS_KEY and settings.AWS_ACCESS_KEY_ID:
                self.stdout.write("Step collect static")
                management.call_command('collectstatic', interactive=False)

        self.stdout.write("Step migrate")
        management.call_command('migrate')

        self.stdout.write("Step svg build")
        management.call_command('svg_build')

        self.stdout.write("Step compile messages")
        management.call_command('compilemessages')

        self.stdout.write("Step clear cache")
        cache.clear()
