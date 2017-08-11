from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField


# Create your models here. 
class Category(models.Model):
	"""
	Description: Holds the different types of categories of stores.
	Store will have one-to-many relation with category
	"""
	name = models.CharField(_('Name'), max_length=254)
	description = models.TextField(_('Description'))

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name


class BaseDetails(models.Model):
	"""
	Base abstract model contains all the feilds for details of franchise and stores
	"""
	name = models.CharField(_('Name'), max_length=254)
	description = models.TextField(_('Description'))
	slug = models.SlugField(unique=True)
	picture = models.ImageField(_('Store Image'),upload_to='Store-picture', null=True, blank=True)

	phone_no = PhoneNumberField(_('Phone Number'))
	website = models.URLField(_('Website'), default='', max_length=256)
	hours = models.CharField(_('Hours'), default="", max_length=256)

	street = models.CharField(_('Street'), default="", max_length=256)
	city = models.CharField(_('City'), default="", max_length=256)
	state = models.CharField(_('State'), default="", max_length=256)
	postal = models.PositiveIntegerField(_('Postal'), default=0)

	return_days = models.PositiveIntegerField(_('Return Days'), default=7)
	
	location = PlainLocationField(based_fields=['city'], zoom=7, null=True)

	class Meta:
		abstract = True


class Franchise(BaseDetails):
	"""
	Description: Model Description
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='franchise')
	category = models.ForeignKey(Category, related_name='franchise', null=True)
	
	def __str__(self):
		return self.name

class Store(BaseDetails):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')

	stand_alone = models.BooleanField(_("Is a stand alone store?"), default=True)
	franchise = models.ForeignKey(Franchise, related_name='store', null=True, blank=True)

	category = models.ForeignKey(Category, related_name='store', null=True, blank=True)

	token = models.CharField(_('Token'), max_length=256, null=True, blank=True)

	def __str__ (self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id: 
			self.slug = slugify(self.name)
			self.name = self.name.title()
			t = Token.objects.create(user=self.user)
			self.token = t.key
		super(Store, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('store:store_detail', kwargs={'slug':self.slug})

	@property
	def get_lat(self):
		"""
		Splits and Returns the first part of the location(latitude)
		"""
		return self.location.split(',')[0]
	
	def get_lat_admin(self):
		"""
		Used to display 'Latitude' in the admin, as short_description cannot be
		assigned to @property `get_lat`
		"""
		return self.get_lat
	get_lat_admin.short_description = 'Latitude'

	
	@property
	def get_long(self):
		"""
		Splits and Returns the last part of the location(longitude)
		"""
		return self.location.split(',')[-1]
	
	def get_long_admin(self):
		"""
		Used to display 'Longitude' in the admin, as short_description cannot be
		assigned to @property `get_long`
		"""
		return self.get_long
	get_long_admin.short_description = 'Longitude'


PRODUCT_CHOICES = (
		('F','Franchise'),
		('S','Store'),
	)
class Product(models.Model):
	"""
	Holds the informations about the products of the store
	"""

	type_of_product = models.CharField( max_length=1, choices=PRODUCT_CHOICES,
				help_text="Whether the product belongs to a individual store or a Franchise?")
	store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product', null=True, blank=True)
	store_chain = models.ForeignKey(Franchise, verbose_name="Franchise", related_name='franchise_product', null=True, blank=True)
	name = models.CharField(_('Name'), max_length=256)
	sku = models.CharField(_('SKU'), max_length=100)
	price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
	quantity = models.IntegerField(_("Available Quantity"), default=0)
	tax = models.DecimalField(_("Tax"), max_digits=5, decimal_places=2, default=0.00)
	infinite_quantity = models.BooleanField(_("Infinite Quantity"),
					 default=False,
					 help_text="Is the quantity infinite? ie. Quantity depends on demand.")

	def __str__(self):
		return self.name


