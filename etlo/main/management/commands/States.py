from main.models import Country, State
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get('https://countriesnow.space/api/v0.1/countries/states')
        r = r.json()['data']
        for item in State.objects.all():
            item.delete()
        for item in r:
            for itemm in item['states']:
                print(item['name'])
                if item['name'] != 'Kosovo':
                    cc = State(country = Country.objects.get(symbol = item['iso2'].replace('GR', 'EL').replace('SS', 'SD')) ,name = itemm['name'] , code = itemm['state_code'])
                    cc.save()
            