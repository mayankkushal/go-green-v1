from django.db import models
from django.urls import reverse
from store.models import Store, Product
from django.contrib.auth.models import User

# Create your models here.

class Bill(models.Model):
	'''
	Bills model to hold the basic bills details
	'''
	bill_no = models.CharField(max_length=100, default='', blank=True)
	store = models.ForeignKey(Store, related_name='bill')
	customer = models.ForeignKey(User, related_name='bill', null=True)
	customer_no = models.CharField(max_length=100, default='', blank=True)
	date = models.DateTimeField(auto_now_add=True)
	notified = models.BooleanField(default=False)
	original = models.BooleanField(default=True)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return self.bill_no
		
	"""
	Bill properties
	"""
	@property
	def store_name(self):
		return self.store.name

	@property
	def customer_name(self):
		return self.customer.profile.get_full_name

	def get_total(self):
		"""
		Calculates the overall total of the bill and returns the result
		"""
		sum = 0
		for item in self.items.all():
			sum += item.get_total()
		return sum

	def get_absolute_url(self):
		return reverse('bill_detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
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
	quantity = models.PositiveIntegerField(default=0)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.product.name

	def get_total(self):
		"""
		Calculates the total price of the item with quantity and returns the result
		"""
		return self.quantity * self.product.price

	def save(self, *args, **kwargs):
		self.total = self.get_total()
		super(Item, self).save(*args, **kwargs)