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

	def clean_customer_no(self):
		try:
			profile = Profile.objects.get(phone_no=self.cleaned_data['customer_no'])
		except Profile.DoesNotExist:
			raise forms.ValidationError("Customer phone number not found, cannot proceed with billing. Please start again!")
		return self.cleaned_data
	
	class Meta:
		model = Bill
		fields = ['customer_no',]
		widgets = {
			'customer_no':forms.TextInput(attrs={'readonly':'readonly'})
		}



class ItemForm(forms.ModelForm):

	product_number = forms.CharField(label='Product',required=False, widget=autocomplete.Select2(
				url='product_autocomplete',
				attrs={
					# Set some placeholder
					'data-placeholder': "Product",
					'onchange':"productDetail(value,id, this)"
					},
				),)
	sku_number = forms.CharField(label='SKU',required=False, widget=autocomplete.ListSelect2(
				url='sku_autocomplete',
				attrs={
					# Set some placeholder
					'data-placeholder': "SKU",
					'onchange':"productDetail(value,id, this)"
					},
				),)
	tax = forms.DecimalField(label="Tax", widget=forms.NumberInput(attrs={'readonly':'readonly'}))
	price = forms.DecimalField(label="Price", disabled=True, required=False)
	total = forms.DecimalField(label="Total", 
						disabled=True, 
						required=False,
						widget=forms.NumberInput(attrs={'class':'total'})
					)
	quantity = forms.IntegerField(min_value=1,
					widget=forms.NumberInput(attrs={'oninput':"calculateTotal(this, value)"})
				)
	product_pk = forms.IntegerField(widget=forms.HiddenInput())
	class Meta:
		model = Item
		fields = ['product_number', 'sku_number','sku', 'quantity']
		#exclude = ('bill','product', 'price','sku' 'tax', 'total')
		widgets = {
			'sku': forms.HiddenInput(),
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


class ItemReturnForm(forms.ModelForm):
	class Meta:
		model = Item
		exclude = ('bill',)
		widgets = {
			'product': forms.Select(attrs={'disabled':"on"}),
			'sku': forms.TextInput(attrs={'disabled':"on"}),
			'quantity':forms.NumberInput(attrs={'max':"on", 'oninput':"calculateTotal(this, value)", 'min':"1"},),
			'tax':forms.NumberInput(attrs={'disabled':"on"}),
			'price':forms.NumberInput(attrs={'disabled':"on"}),
			'total':forms.NumberInput(attrs={'disabled':"on", 'class':'total'})
		}
ItemReturnFormSet = inlineformset_factory(Bill, Item, form=ItemReturnForm, extra=0, can_delete=True)


class BillReturnForm(forms.ModelForm):
	class Meta:
		model = Bill
		fields = ['customer_no', 'bill_no', 'total']
		widgets = {
			'customer_no':forms.TextInput(attrs={'readonly':'readonly'}),
			'bill_no':forms.TextInput(attrs={'readonly':'readonly'}),
			'total':forms.NumberInput(attrs={'readonly':'readonly'}),
		}