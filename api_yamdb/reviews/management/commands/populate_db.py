import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import DATA_DIR
from users.models import User


class Command(BaseCommand):
    help = 'Заполняет таблицу из csv файла'

    def add_arguments(self, parser):
        parser.add_argument('tables', nargs='+', type=str)

    def handle(self, *args, **options):
        for table in options['tables']:
            self.stdout.write(
                self.style.SUCCESS(f'Обрабатываемая таблица: {table}')
            )
            filename = os.path.join(DATA_DIR, table + '.csv')
            self.stdout.write(filename)
            users = []
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    users.append(User(**row))
            self.stdout.write(
                f'Записей до вставки: {User.objects.all().count()}'
            )
            User.objects.bulk_create(users)
            self.stdout.write(
                f'Записей после вставки: {User.objects.all().count()}'
            )
