from main.models import Country, State
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Country.objects.all():
            try: 
                r = requests.post('https://countriesnow.space/api/v0.1/countries/flag/images', data={'iso2': item.symbol.replace('GR', 'EL').replace('SS', 'SD')})
                r = r.json()['data']['flag']
                item.image = r
                item.save()
            except:
                item.image = ''
                item.save()