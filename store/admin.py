from django.contrib import admin
from .models import Store, Product, Category

# Register your models here.


class ProductInline(admin.TabularInline):

	'''
		Tabular Inline View for Product
	'''
	model = Product
	

class StoreAdmin(admin.ModelAdmin):
	list_display = ('name', 'city', 'state', 'category')
	list_filter = ('city', 'state')
	raw_id_fields = ('store','category')
	fieldsets = (
		('Details', {
			'fields': (('store','category'),('name', 'phone_no'),'description', 'picture')
		}),
		('Address', {
			'fields': ('street', ('city', 'state', 'postal'), 'location')
		}),
		('Optional', {
			'fields': ('website', 'hours')
		}),
		('API', {
			'fields': ('token',)
		})
	)
	inlines = (ProductInline, )


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(admin.ModelAdmin):
	'''
		Admin View for Category
	'''
	search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	'''
		Admin View for Product
	'''
	list_display = ('name', 'store', 'price')
	list_filter = ('store',)
	raw_id_fields = ('store',)
	search_fields = ('name','store')

admin.site.register(Product, ProductAdmin)