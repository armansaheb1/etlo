from main.models import Country, State, City
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        i = 0
        state = State.objects.filter(city = False)
        for item in State.objects.filter(city = False):
            if not len(City.objects.filter(state = item)):
                try:
                    r = requests.post('https://countriesnow.space/api/v0.1/countries/state/cities', data={'country': item.country.name.replace('Congo', 'Congo'), "state": item.name})
                    r = r.json()['data']
                    for itemm in r:
                        cc = City(name = itemm, state = item)
                        cc.save()
                    print(item.country.name, i/state.count() * 100)
                    i = i+1
                    item.city = True
                    item.save()
                except:
                    print('-', item.country.name, i/state.count() * 100)
            