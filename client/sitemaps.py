from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from store.models import Store
from blog.models import Article

from django.apps import apps as django_apps
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured

class StoreSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.7

	def items(self):
		return Store.objects.all()

class BlogSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return Article.objects.all()

class StaticSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.1

	item_list = [
		'qr_scanner',
		'auth_login',
		'registration_register',
	]
	def items(self):
		return self.item_list

	def location(self, item):
		return reverse(item)


class FlatPageSitemap(Sitemap):
	changefreq = 'weekly'
	priority = 0.1
	
	def items(self):
		if not django_apps.is_installed('django.contrib.sites'):
			raise ImproperlyConfigured("FlatPageSitemap requires django.contrib.sites, which isn't installed.")
		Site = django_apps.get_model('sites.Site')
		current_site = Site.objects.get_current()
		return current_site.flatpage_set.filter(registration_required=False)