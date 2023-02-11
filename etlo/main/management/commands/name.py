from main.models import CustomUser
from django.core.management.base import BaseCommand, CommandError
import requests
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in CustomUser.objects.all():
            if item.first_name == 'test':
                item.first_name = 'test' + str(random.randint(1, 100))
            if item.last_name == 'test':
                item.last_name = 'test' + str(random.randint(1, 100))
            if not item.email:
                item.email = f'test{str(random.randint(1, 100))}@test.test'
            item.save()
