from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView


from .forms import StoreForm, ProductForm
from .models import Store, Product
# Create your views here.

class StoreCreate(CreateView):
	form_class = StoreForm
	model = Store

class StoreUpdate(UpdateView): 
	form_class = StoreForm
	model = Store
	context_object_name = 'store'


class StoreLocator(TemplateView):
	template_name = 'store/locator.html'


class ProductCreate(CreateView):
	form_class = ProductForm
	model = Product
	success_url = "/"
