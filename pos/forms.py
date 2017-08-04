from django import forms
from django.forms import BaseInlineFormSet
from django.forms import inlineformset_factory

from bills.models import Item, Bill
from client.models import Profile

import re

from dal import autocomplete


class BaseItemInlineFormset(BaseInlineFormSet):
	pass

class BillForm(forms.ModelForm):
	class Meta:
		model = Bill
		fields = ['customer_no',]
		widgets = {
			'customer_no':forms.TextInput(attrs={'readonly':'readonly'})
		}

class ItemForm(forms.ModelForm):
	product_number = forms.CharField(label='Product', widget=autocomplete.Select2(
				url='product_autocomplete',
				attrs={
					# Set some placeholder
					'data-placeholder': "Product",
					'onchange':"productDetail(value,id)"
					},
				),)
	tax = forms.DecimalField(label="Tax", widget=forms.NumberInput(attrs={'readonly':'readonly'}))
	price = forms.DecimalField(label="Price", disabled=True, required=False)
	total = forms.DecimalField(label="Total", disabled=True, required=False)
	class Meta:
		model = Item
		fields = ['product_number', 'sku', 'quantity']
		exclude = ('bill','product', 'price', 'tax', 'total')
		widgets = {
			'quantity': forms.NumberInput(
				attrs={
					'oninput':"calculateTotal(this, value)",
				}
			)
		}

ItemFormSet = inlineformset_factory(Bill, Item, form=ItemForm, extra=1, can_delete=True)

class CustomerPhoneNumberForm(forms.Form):
	customer_phone_no = forms.CharField(label='Customer Number')

	def clean_customer_phone_no(self):
		cus_no = self.cleaned_data['customer_phone_no']
		try:
			if not re.search(r'[0-9]{10}$', cus_no):
				raise forms.ValidationError("Invalid phone number")
		except ValueError:
			pass
		try:
			if not Profile.objects.filter(phone_no=cus_no).exists():
				raise forms.ValidationError("Customer not found, please check the phone number")
		except KeyError:
			pass
		return self.cleaned_data