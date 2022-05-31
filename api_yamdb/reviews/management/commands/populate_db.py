from django.core.management.base import BaseCommand
import csv
import os

from api_yamdb.settings import DATA_DIR


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
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    self.stdout.write(row['id'])
