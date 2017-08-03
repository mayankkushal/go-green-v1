from django import template

register = template.Library()


@register.simple_tag
def get_store(name):
	try:
		store = Store.objects.get(name=name)
		return store.get_absolute_url()
	except:
		store = None
		return '#'