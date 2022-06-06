import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

FILE_MODEL_DICT = {
    'users': User,
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'review': Review,
    'comments': Comment,
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
            filename = os.path.join(settings.DATA_DIR, table + '.csv')
            self.stdout.write(filename)
            Model = FILE_MODEL_DICT[table]
            data_list = []
            with open(filename, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
                for row in reader:
                    if table == 'titles':
                        row['category'] = Category.objects.get(
                            pk=row['category']
                        )
                    if table == 'review':
                        print(row)
                        row['author'] = User.objects.get(
                            pk=row['author']
                        )
                    if table == 'comments':
                        print(row)
                        row['author'] = User.objects.get(
                            pk=row['author']
                        )
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
