from django.db import models
from django.urls import reverse
from store.models import Store, Product
from django.contrib.auth.models import User

import decimal

# Create your models here.

class Bill(models.Model):
	'''
	Bills model to hold the basic bills details
	'''
	bill_no = models.CharField(max_length=100, default='', blank=True)
	store = models.ForeignKey(Store, related_name='bill')
	#customer = models.ForeignKey(User, related_name='bill', null=True)
	customer_no = models.CharField(max_length=100, default='', blank=True)
	date = models.DateTimeField(auto_now_add=True)
	notified = models.BooleanField(default=False)
	original = models.BooleanField(default=True)
	sale_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return self.bill_no

	@property
	def store_name(self):
		return self.store.name

	@property
	def customer_name(self):
		return self.get_customer.profile.get_full_name

	@property
	def get_customer(self):
		return User.objects.get(profile__phone_no=self.customer_no)

	def get_tax_amount(self):
		"""
			Calculate the total tax amount of the bill, by iterating over 
			oll the items of the bill and calling `get_tax_amount()` of the
			`Item` model
		"""
		tax_amount = decimal.Decimal(0.0)
		for item in self.items.all():
			tax_amount += item.get_tax_amount()
		return tax_amount

	def get_sale_value(self):
		"""
		Calculates the sale value of the bill.
		ie. the amount without adding the tax
		"""
		sum = 0
		for item in self.items.all():
			sum += item.get_total()
		return sum

	def get_total(self):
		"""
		Calculates the overall total of the bill by adding `sale_value` and `tax_amount`
		"""
		sum = 0
		return self.sale_value + self.tax_amount

	def get_absolute_url(self):
		return reverse('bill_detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		self.sale_value = self.get_sale_value()
		self.tax_amount = self.get_tax_amount()
		self.total = self.get_total()
		super(Bill, self).save(*args, **kwargs)



class Item(models.Model):
	"""
	Individual product will have many-to-one relation to the bill. 
	Need to be sent together in the JSON of the bill.
	"""
	bill = models.ForeignKey(Bill, related_name='items', null=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True)
	sku = models.CharField(max_length=100, null=True)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.product.name

	def get_total(self):
		"""
		Calculates the total price of the item without tax, and returns the result
		"""
		return self.quantity * self.product.price

	def get_tax_amount(self):
		"""
			Calculates the tax_amount if the product has tax
		"""
		tax_amount = decimal.Decimal(0.0)
		if self.product.tax is not 0:
			tax_amount = (self.price*(self.tax/100))*self.quantity
		return tax_amount

	def update_quantity(self):
		"""
		Substracts the quantity of the bill item from the total quantity of the product.
		The new quantity is updated
		"""
		if not self.product.infinite_quantity:
			self.product.quantity = self.product.quantity - self.quantity
			self.product.save()

	def save(self, *args, **kwargs):
		if not self.id:
			self.price = self.product.price
			self.tax = self.product.tax
			self.total = self.get_total()
			self.update_quantity()
		super(Item, self).save(*args, **kwargs)