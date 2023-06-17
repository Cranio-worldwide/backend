import json
from pathlib import Path

from django.core.management.base import BaseCommand

from ...models import StaticContent


class Command(BaseCommand):
    help = 'Fills the DB with json-files with static content for frontend'

    def handle(self, *args, **kwargs):
        files = (
            ('main', 'main'),
            ('search', 'search'),
        )
        counter, objects = 0, []
        for file, page_name in files:
            counter += 1
            self.stdout.write(f'{"---"*40}\n Opening files: {file}_##.json')
            try:
                with open(Path('static', 'import_db', f'{file}_ru.json'),
                          encoding='utf-8') as f:
                    data_ru = json.load(f)
                with open(Path('static', 'import_db', f'{file}_en.json')) as f:
                    data_en = json.load(f)
                objects.append(StaticContent(
                    name=page_name,
                    fields_ru=data_ru,
                    fields_en=data_en
                ))
            except FileNotFoundError:
                self.stderr.write(f'File {file}_##.json not found')
                continue
        try:
            StaticContent.objects.bulk_create(objects,
                                              ignore_conflicts=True)
            self.stdout.write(f'Added objects: {len(objects)} / {counter}')
        except ValueError:
            self.stderr.write('Files contained errors, process is stopped')
