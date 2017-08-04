from django.shortcuts import render
from django.db import transaction
from django.views.generic import CreateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse

import simplejson as json

from dal import autocomplete

from bills.models import Bill, Item
from client.models import Profile
from store.models import Store, Product
from .forms import BillForm, ItemFormSet, CustomerPhoneNumberForm
# Create your views here.

class CreateBill(CreateView):
	"""
		Creates a new bill,
	"""
	form_class = BillForm
	model = Bill
	template_name = 'pos/billing_page.html'
	success_url = reverse_lazy('index')

	def get_initial(self):
		no = self.request.session.get('cus_no')
		self.request.session['cus_no'] = None
		return { 'customer_no': no,}

	def get_context_data(self, **kwargs):
		context = super(CreateBill, self).get_context_data(**kwargs)
		if self.request.POST:
			context['items'] = ItemFormSet(self.request.POST)
		else:
			context['items'] = ItemFormSet()
		return context

	def form_valid(self, form):
		context = self.get_context_data()
		items = context['items']
		
		with transaction.atomic():
			profile = Profile.objects.get(phone_no=form.cleaned_data['customer_no'])
			form.instance.customer = User.objects.get(profile=profile)
			store = Store.objects.get(store=self.request.user)
			form.instance.store = store
			self.object = form.save()
		
		if items.is_valid():
			for item in items:
				item.instance.product = Product.objects.get(pk=item.cleaned_data['product_number'])
				item.instance.bill = self.object
				item.save()

		return super(CreateBill, self).form_valid(form)


class ProductAutocomplete(autocomplete.Select2QuerySetView):
	"""
		Autocompletes the product field in the billing page
	"""
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return Product.objects.none()

		store = Store.objects.get(store=self.request.user)
		qs = Product.objects.filter(store=store)
		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


def product_detail(request):
	"""
		Returns the details of the product selected in the product field in the
		billing page
	"""
	if request.method == 'GET':
		try:
			product = Product.objects.get(pk=request.GET.get('product_pk'))
		except Product.DoesNotExist:
			product = None

		if product:
			data = {
				'sku':product.sku,
				'price':product.price,
				'tax':product.tax,
			}
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			return HttpResponse()


class BillingStart(FormView):
	success_url = reverse_lazy('billing')
	template_name = 'pos/billing_start.html'
	form_class = CustomerPhoneNumberForm

	def form_valid(self, form):
		"""
		If the form is valid, add the customer number to the session.
		"""
		no = form.data.get('customer_phone_no')
		self.request.session['cus_no'] = no
		return super(BillingStart, self).form_valid(form)


