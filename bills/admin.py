from django.contrib import admin
from .models import Bill, Item
# Register your models here.


class ItemInline(admin.TabularInline):
	model = Item

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
	"""
	Costomized Bill admin. 
	Showing details in bill form
	"""
	list_display = ('bill_no', 'date', 'total')
	list_filter = ('store', )
	raw_id_fields = ('store', )
	inlines = [ItemInline,]

admin.site.register(Item)