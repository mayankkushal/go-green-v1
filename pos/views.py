from django.shortcuts import render
from django.db import transaction
from django.views.generic import CreateView, UpdateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

import simplejson as json

from dal import autocomplete

from bills.models import Bill, Item
from client.models import Profile
from store.models import *
from .forms import BillForm, ItemFormSet, CustomerPhoneNumberForm, ItemReturnFormSet, BillReturnForm
# Create your views here.

class CreateBill(CreateView):
	"""
		Creates a new bill,
	"""
	form_class = BillForm
	model = Bill
	template_name = 'pos/billing_page.html'

	def get_initial(self):
		"""
			Passes the customer number from the session as initial data to the
			form and clears the session as it cannot be further used.
		"""
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
			profile = Profile.objects.get(phone_no=form.data['customer_no'])
			form.instance.customer_no = form.data['customer_no']
			form.instance.customer = User.objects.get(profile=profile)
			store = Store.objects.get(user=self.request.user)
			form.instance.store = store
			self.object = form.save()
		
		if items.is_valid():
			for item in items:
				try: # Doesn't save the product when the product_pk is empty
					item.instance.product = Product.objects.get(pk=item.cleaned_data['product_pk'])
					item.instance.bill = self.object
					item.save()
				except KeyError:
					pass

		return super(CreateBill, self).form_valid(form)

	def get_success_url(self):
		"""
			Returns the bill details page
		"""
		return reverse_lazy('bill_detail', kwargs={'pk': self.object.pk})


class ProductAutocomplete(autocomplete.Select2QuerySetView):
	"""
		Autocompletes the product field in the billing page
	"""
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated():
			return Product.objects.none()

		store = Store.objects.get(user=self.request.user)
		try:
			franchise = store.franchise
		except:
			franchise = None

		qs = Product.objects.filter(store_chain=franchise) if franchise else Product.objects.filter(store=store)
		
		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


class SKUAutocomplete(autocomplete.Select2ListView):
	def get_list(self):

		store = Store.objects.get(user=self.request.user)
		try:
			franchise = store.franchise
		except:
			franchise = None
		if franchise:
			qs =  Product.objects.filter(store_chain=franchise).values_list('sku', flat=True)
		else: 
			qs = Product.objects.filter(store=store).values_list('sku', flat=True)

		return qs



def product_detail(request):
	"""
		Returns the details of the product selected in the product field in the
		billing page
	"""
	if request.method == 'GET':
		try:
			product = Product.objects.get(pk=request.GET.get('product_pk'))
		except:
			product = Product.objects.get(sku=request.GET.get('product_pk'))

		if product:
			data = {
				'sku':product.sku,
				'price':product.price,
				'tax':product.tax,
				'num':product.pk,
				'name':product.name,
			}
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			return HttpResponse()


class ReturnBill(UpdateView):

	model = Bill
	form_class = BillReturnForm
	template_name = 'pos/return_page.html'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		items = ItemReturnFormSet(instance = self.object)
		return self.render_to_response(self.get_context_data(form = form, items = items))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		items = ItemReturnFormSet(self.request.POST, instance=self.object)

		if (form.is_valid() and items.is_valid()):
		  return self.form_valid(form, items)
		return self.form_invalid(form, items)

	def form_valid(self, form, items):
		
		# Makes the old bill un-editable
		old_bill = self.get_object()
		old_bill.editable = False
		old_bill.save()

		old_total = old_bill.total # Total of the previous bill

		# Saves a new copy of bill with the same bill number.
		# Bill number is assigned in the post_save signal.
		obj = form.save(commit=False)
		obj.pk = None
		obj.customer_no = form.data['customer_no']
		obj.bill_no = form.data['bill_no']
		obj.original = False
		obj.save()
		
		for item in items:
			if item.instance.quantity > 0:
				item.instance.pk = None
				item.instance.bill = obj
				item.save()
		obj.save()

		# Finalinizing the total return amount, it'll be stored in the new bill
		return_amount = old_total - obj.get_total()
		obj.return_amount = return_amount
		obj.save()

		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, items):
		return self.render_to_response(self.get_context_data(form=form, items=items))

	def get_success_url(self):
		"""
			Returns the bill details page
		"""
		return reverse_lazy('bill_detail', kwargs={'pk': self.object.pk})
