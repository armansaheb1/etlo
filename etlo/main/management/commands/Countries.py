from main.models import Country
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get('https://countriesnow.space/api/v0.1/countries/codes')
        r = r.json()['data']
        for item in Country.objects.all():
            item.delete()
        for item in r:
            cc = Country(name = item['name'] , dial_code = item['dial_code'].replace(' ', '').replace('+', ''), symbol = item['code'])
            cc.save()