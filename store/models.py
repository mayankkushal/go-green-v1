from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField
from django.contrib.auth.hashers import make_password


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


CATEGORY_CHOICES = (
		('P','Parent'),
		('S','Sub'),
	)
class ProductCategory(models.Model):
	"""
	Description: Category of defferent Products. Can have multiple sub-category
	"""
	name = models.CharField(_('Name'), max_length=254)
	category_relation = models.CharField(_('Category Relation'), max_length=1, choices=CATEGORY_CHOICES,
				help_text="Whether the Category is first in line or sub of any other Category.")
	parent_category = models.ForeignKey('ProductCategory', related_name='sub_category',
							  null=True, blank=True)

	def __str__(self):
		return self.name


class FranchiseType(models.Model):
	name = models.CharField(_('Name'), max_length=254)

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

	mgr_password = models.CharField(_('Manager Password'), max_length=150, blank=True, null=True)

	return_days = models.PositiveIntegerField(_('Return Days'), default=7)
	
	location = PlainLocationField(based_fields=['city'], zoom=7, null=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		self.mgr_password = make_password(self.mgr_password)
		super(BaseDetails, self).save(*args, **kwargs)


class Franchise(BaseDetails):
	"""
	Description: A chain of many stores, borrows the same details as a normal store.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='franchise')
	category = models.ForeignKey(Category, related_name='franchise', null=True)
	
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id: 
			self.slug = slugify(self.name)
			self.name = self.name.title()
			self.city = self.city.title()
			self.state = self.state.title()
		super(Franchise, self).save(*args, **kwargs)


class Store(BaseDetails):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')

	stand_alone = models.BooleanField(_("Is a stand alone store?"), default=True)
	franchise_type = models.ForeignKey(FranchiseType, related_name='store', null=True, blank=True)
	
	franchise = models.ForeignKey(Franchise, related_name='store', null=True, blank=True)

	category = models.ForeignKey(Category, related_name='store', null=True, blank=True)

	token = models.CharField(_('Token'), max_length=256, null=True, blank=True)

	def __str__ (self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id: 
			self.slug = slugify(self.name)
			self.name = self.name.title()
			self.city = self.city.title()
			self.state = self.state.title()
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
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product',
									 null=True, blank=True)
	store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_product',
								 null=True, blank=True)
	store_chain = models.ForeignKey(Franchise, verbose_name="Franchise", related_name='franchise_product', null=True, blank=True)
	name = models.CharField(_('Name'), max_length=256)
	sku = models.CharField(_('SKU'), max_length=100)
	price = models.DecimalField(_('Price'), max_digits=10, decimal_places=2)
	quantity = models.IntegerField(_("Available Quantity"), default=0, blank=True)
	discount = models.DecimalField(_('Discount'), max_digits=5, decimal_places=2, default=0.00)
	tax = models.DecimalField(_("Tax"), max_digits=5, decimal_places=2, default=0.00)
	infinite_quantity = models.BooleanField(_("Infinite Quantity"),
					 default=False,
					 help_text="Is the quantity infinite? ie. Quantity depends on demand.")

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id: 
			self.name = self.name.title()
		super(Product, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('store:update_product', kwargs={'pk':self.pk})


#To be implemented in the future
# class Staff(models.Model):
# 	STAFF_CHOICES = (
# 		('I','Inventory Manager'),
# 		('B','Billing Clerk'),
# 	)

# 	user = models.OneToOneField(User, related_name="store_staff",on_delete=models.CASCADE)
# 	store = models.OneToOneField(Store, related_name="staff", on_delete=models.CASCADE)
# 	type_of_staff = models.CharField(max_length=1, choices=STAFF_CHOICES)

# 	class Meta:
# 		verbose_name = "Staff"
# 		verbose_name_plural = "Staffs"

# 	def __str__(self):
# 		return self.user.first_name