import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from users.models import Specialist
from api.models import Address, Service, City, Country


class Command(BaseCommand):
    help = 'Fills the database with data from csv-file in static folder'

    def handle(self, *args, **kwargs):
        FILE_HANDLE = (
            ('countries.csv', Country),
            ('cities.csv', City),
            ('users.csv', Specialist),
            ('addresses.csv', Address),
            ('services.csv', Service),
        )
        for file, model in FILE_HANDLE:
            self.stdout.write(f'{"---"*40}\n Открываем файл {file}')
            file_path = Path('static', 'import_db', file)
            if not file_path.exists():
                self.stderr.write(f'Файл {file} не найден')
                continue
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                self.stdout.write(f'Начинаем импорт из файла {file}')
                reader = csv.DictReader(f, delimiter=';')
                counter = 0
                objects_to_create = []
                if file == 'users.csv':
                    for row in reader:
                        counter += 1
                        args = dict(**row)
                        Specialist.objects.create_user(**args)
                    self.stdout.write(f'Добавлено объектов: {counter}')
                else:
                    for row in reader:
                        counter += 1
                        args = dict(**row)
                        try:
                            objects_to_create.append(model(**args))
                        except TypeError:
                            self.stderr.write('Неверный заголовок в csv-файле')
                            break
                    try:
                        model.objects.bulk_create(objects_to_create,
                                                  ignore_conflicts=True)
                        self.stdout.write(
                            f'Добавлено объектов: {len(objects_to_create)}; '
                            f'строк в документе: {counter}')
                    except ValueError:
                        self.stderr.write('Ошибка заполнения csv')
