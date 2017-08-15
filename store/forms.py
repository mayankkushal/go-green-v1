from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Store, Product, Franchise

class StoreForm(forms.ModelForm):
	class Meta:
		model = Store
		fields = ['picture', 'name', 'description', 'phone_no']
		exclude = ['slug', 'location', 'city', 'token']
		widgets = {
			'phone_no' : PhoneNumberInternationalFallbackWidget
		}

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude = ('type_of_product', 'store', 'store_chain')

