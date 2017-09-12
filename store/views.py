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
from client.mixins import StatementMixin
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
	success_url = reverse_lazy('store:product_list')

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
	success_url = reverse_lazy('store:product_list')

	def get_queryset(self):
		queryset = super(ProductUpdate, self).get_queryset()
		try:
			store = self.request.user.store
			q = queryset.filter(store__user=self.request.user)
		except Store.DoesNotExist:
			q = queryset.filter(store_chain__user=self.request.user)
		return q


class ProductListView(ListView):
	model = Product
	paginate_by = 20
	
	def get_context_data(self, **kwargs):

		context = super(ProductListView, self).get_context_data(**kwargs)

		try:
			store = self.request.user.store
			product_list = Product.objects.filter(store__user=self.request.user)
		except Store.DoesNotExist:
			product_list = Product.objects.filter(store_chain__user=self.request.user)

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


class StoreStatement(StatementMixin, TemplateView):
	template_name = "store/statement.html"

	def get_context_data(self, **kwargs):
		context = super(StoreStatement, self).get_context_data(**kwargs)

		week_start, week_end = self.get_week_dates()
		month_start, month_end = self.get_month_dates()
		year_start, year_end = self.get_year_dates()

		store = self.request.user.store
		
		daily_bill = self.get_daily_bill(store=store)
		weekly_bill = self.get_bill_in_range(week_start, week_end, store=store)
		monthly_bill = self.get_bill_in_range(month_start, month_end, store=store)
		yearly_bill = self.get_bill_in_range(year_start, year_end, store=store)

		context['daily_count'] = len(daily_bill)
		context['weekly_count'] = len(weekly_bill)
		context['monthly_count'] = len(monthly_bill)
		context['yearly_count'] = len(yearly_bill)

		context['daily_total'] = self.get_bill_total(daily_bill)
		context['weekly_total'] = self.get_bill_total(weekly_bill)
		context['monthly_total'] = self.get_bill_total(monthly_bill)
		context['yearly_total'] = self.get_bill_total(yearly_bill)

		context['daily_store'] = self.get_unique_customers(daily_bill)
		context['weekly_store'] = self.get_unique_customers(weekly_bill)
		context['monthly_store'] = self.get_unique_customers(monthly_bill)
		context['yearly_store'] = self.get_unique_customers(yearly_bill)

		return context
