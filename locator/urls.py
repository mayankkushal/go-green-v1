from django.conf.urls import url

from .views import locator, locations


urlpatterns = [
    url(r'^$', locator, name='locator'),
    url(r'^locations/$', locations, name='locations'),
]

