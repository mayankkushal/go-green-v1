from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import reverse_lazy

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

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



@method_decorator(login_required, name='dispatch')
class ProductCreate(CreateView):
	form_class = ProductForm
	model = Product
	success_url = "/"

	def form_valid(self, form):
		if self.request.user.store.stand_alone:
			form.instance.type_of_product = 'S'
			form.instance.store = self.request.user.store
		else:
			form.instance.type_of_product = 'F'
			form.instance.store_chain = self.request.user.franchise 
		return super(ProductCreate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdate(UpdateView):
	form_class = ProductForm
	model = Product

	def get_queryset(self):
		queryset = super(ProductUpdate, self).get_queryset()
		return queryset.filter(store__user=self.request.user)


class ProductListView(ListView):
	model = Product
	paginate_by = 20
	
	def get_context_data(self, **kwargs):

		context = super(ProductListView, self).get_context_data(**kwargs)
		product_list = Product.objects.filter(store__user=self.request.user)

		paginator = Paginator(product_list, self.paginate_by)

		page = self.request.GET.get('page')
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		context['product_list'] = products
				
		return context

class ProductDelete(DeleteView):
	model = Product
	success_url = reverse_lazy('store:product_list')

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(ProductDelete, self).get_object()
		if not obj.store == self.request.user.store:
			raise Http404
		return obj