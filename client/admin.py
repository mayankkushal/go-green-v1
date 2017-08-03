from django.contrib import admin
from .models import Profile, Banner, SlideShowImage, User, Newsletter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class ProfileInline(admin.StackedInline):
	model = Profile
	can_delete = False
	#filter_horizontal = ['phone_no']  # example: ['tlf', 'country',...]
	verbose_name_plural = 'profiles'
	fk_name = 'user'


class UserAdmin(UserAdmin):
	inlines = (ProfileInline, )
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
	list_filter = ('is_staff', 'is_superuser', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	"""
	Customized profile admin.
	Made to look like the User Admin page
	"""
	list_display = ('full_name','email', 'phone_no', 'customer_number')

	def full_name(self, obj):
		return obj.get_full_name
	full_name.short_description = 'Name'

	def email(self, obj):
		return obj.user.email

	def customer_number(self, obj):
		return obj.user.id


class ImageInline(admin.TabularInline):
	model = SlideShowImage
	readonly_fields = ['admin_image']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
	"""
	Banner and images shown together
	"""
	inlines = [ImageInline,]


admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.register(User, UserAdmin)  # Register User with this inline profile

from djangoseo.admin import register_seo_admin
from .seo import MyMetadata

register_seo_admin(admin.site, MyMetadata)


admin.site.register(Newsletter)