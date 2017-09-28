from django.contrib import admin
from .models import Store, Product, Category, Franchise, FranchiseType, ProductCategory
from guardian.admin import GuardedModelAdmin


# Register your models here.

class FranchiseAdmin(admin.ModelAdmin):
	'''
		Admin View for Franchise
	'''
	list_display = ('name', 'city', 'state', 'category')
	list_filter = ('city', 'state')
	fieldsets = (
		('Details', {
			'fields': ('user',('name', 'phone_no'),'description', 'picture')
		}),
		('Address', {
			'fields': ('street', ('city', 'state', 'postal'), 'location')
		}),
		('Policies', {
			'fields': (('return_days'), 'category')
		}),
		('Optional', {
			'fields': ('website', 'hours','mgr_password')
		}),
	)

admin.site.register(Franchise, FranchiseAdmin)

class StoreAdmin(GuardedModelAdmin):
	list_display = ('name', 'city', 'state', 'category', 'stand_alone')
	list_filter = ('city', 'state', 'stand_alone')
	raw_id_fields = ('user','category')
	fieldsets = (
		('Details', {
			'fields': ('user',('name', 'phone_no'),'description', 'picture')
		}),
		('Address', {
			'fields': ('street', ('city', 'state', 'postal'), 'location')
		}),
		('Policies', {
			'fields': (('return_days', 'stand_alone',), 'franchise_type', 'franchise', 'category')
		}),
		('Optional', {
			'fields': ('website', 'hours','mgr_password')
		}),
		('API', {
			'fields': ('token',)
		})
	)


admin.site.register(Store, StoreAdmin)


class CategoryAdmin(admin.ModelAdmin):
	'''
		Admin View for Category
	'''
	search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)
admin.site.register(FranchiseType)

class ProductCategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for ProductCategory
    '''
    list_display = ('name', 'category_relation', 'parent_category')
    list_filter = ('category_relation',)
    search_fields = ('name',)

admin.site.register(ProductCategory, ProductCategoryAdmin)