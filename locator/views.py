import json

from django.template.response import TemplateResponse
from django.http import HttpResponse

from .models import Location
from store.models import Store

def locator(request):
    return TemplateResponse(request, 'locator/locator.html')


def locations(request):
    locations = Store.objects.all()
    formatted_locations = []
    count = 1
    for location in locations:
        formatted_locations.append({
            'id': str(count),
            'name': location.name,
            'lat': location.get_lat,
            'lng': location.get_long,
            'category':location.category.name,
            'address': location.street,
            'address2': '',
            'city': location.city,
            'state': location.state,
            'postal': location.postal,
            'phone': location.phone_no.national_number,
            'web': location.website,
            'hours1': location.hours,
            'hours2': '',
            'hours3': '',
        })
        count += 1
    return HttpResponse(json.dumps(formatted_locations),
                        content_type='application/json')
