import os

import xlrd
from django.conf import settings
from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Run tasks'

    def handle(self, *args, **options):
        book = xlrd.open_workbook(os.path.join(settings.BASE_DIR, 'users.xlsx'))
        sheet = book.sheet_by_index(0)
        for cell in range(1, sheet.nrows):
            try:
                User.objects.create(email=sheet.cell_value(cell, 1), name=sheet.cell_value(cell, 0))
                print(f'Added {sheet.cell_value(cell, 0)} {sheet.cell_value(cell, 1)}')
            except Exception:
                continue
