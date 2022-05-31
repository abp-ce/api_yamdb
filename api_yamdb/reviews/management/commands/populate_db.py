import csv
import os

from django.core.management.base import BaseCommand

from api_yamdb.settings import DATA_DIR
from users.models import User

FILE_MODEL_DICT = {
    'users': User,
}


class Command(BaseCommand):
    help = 'Заполняет таблицу из csv файла'

    def add_arguments(self, parser):
        parser.add_argument('tables', nargs='+', type=str)
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Удаляет строки в таблице, которые есть в csv',
        )

    def handle(self, *args, **options):
        for table in options['tables']:
            self.stdout.write(
                self.style.SUCCESS(f'Обрабатываемая таблица: {table}')
            )
            filename = os.path.join(DATA_DIR, table + '.csv')
            self.stdout.write(filename)
            Model = FILE_MODEL_DICT[table]
            data_list = []
            with open(filename) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                for row in reader:
                    data_list.append(Model(**row))
            if options['delete']:
                self.stdout.write(
                    f'Записей до удаления: {Model.objects.all().count()}'
                )
                for data in data_list:
                    Model.objects.filter(pk=data.id).delete()
                self.stdout.write(
                    f'Записей после удаления: {Model.objects.all().count()}'
                )
            else:
                self.stdout.write(
                    f'Записей до вставки: {Model.objects.all().count()}'
                )
                Model.objects.bulk_create(data_list)
                self.stdout.write(
                    f'Записей после вставки: {Model.objects.all().count()}'
                )
