from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from location_field.models.plain import PlainLocationField

# Create your models here.

class Profile(models.Model):
	GENDER_CHOICES = (
	('M', 'Male'),
	('F', 'Female'),
	('O', 'Other'),
	)

	user = models.OneToOneField(User, related_name="profile")
	first_name = models.CharField(_('First Name'),max_length=254, default="")
	last_name = models.CharField(_('Last Name'),max_length=254, default="")
	phone_no = PhoneNumberField(_('Phone number'),help_text="Choose your country code by clicking on the menu above.", unique=True)
	dob = models.DateField(_('Date of Birth'), blank=True, null=True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=50, default='M')
	profile_pic = models.ImageField(_('Profile Picture'),upload_to='profile-picture', null=True, blank=True)
	address = models.TextField(_('Address'), default="")

	def __str__(self):
		return self.first_name + " " + self.last_name

	def get_absolute_url(self):
		return reverse('profile-view', kwargs={'slug':self.user.profile.phone_no.national_number})

	def save(self, *args, **kwargs):
		if not self.id:
			self.first_name = self.first_name.title()
			self.last_name = self.last_name.title()
		super(Profile, self).save(*args, **kwargs)
	
	"""
	Model properties
	"""
	@property
	def get_full_name(self):
		return self.first_name+" "+self.last_name


class Banner(models.Model):
	"""
	Holds all kinds of banners, crousels etc
	"""
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name


class SlideShowImage(models.Model):
	"""
	Main page slideshow with url
	"""
	slideshow = models.ForeignKey(Banner)
	image = models.ImageField(upload_to='slideshow')
	url = models.URLField(blank=True)
	desc = models.CharField(max_length=300, blank=True)

	def __str__(self):
		return self.image.name

	def admin_image(self):
		'''
		Display thumbnail in admin page
		'''
		return '<img src="%s" style="width:70px; height:70px;"/>' % self.image.url

	admin_image.short_description = 'Image'
	admin_image.allow_tags = True


class Newsletter(models.Model):
	"""
	Description: Newsletter Description

	A simple newsletter, it holds the email of the of the users.
	
	#to be done
	(and if the user is authenticated, adds
	the user to the ono-to-one feild)
	"""
	email = models.EmailField(max_length=254, blank=False)
	
	def __str__(self):
		return self.email
	
	class Meta:
		pass

