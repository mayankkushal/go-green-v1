from .models import Bill
import django_filters
from datetimewidget.widgets import DateWidget


class BillFilter(django_filters.FilterSet): 

	dateTimeOptions = {'format': 'mm/dd/yyyy', 'todayHighlight': True,}


	items__product__name = django_filters.CharFilter(lookup_expr='icontains', label='Product')
	#store__name = django_filters.CharFilter(lookup_expr='icontains', label='Store')
	total__gte = django_filters.NumberFilter(lookup_expr='gte', name='total', label='Total(From)')
	total__lte = django_filters.NumberFilter(lookup_expr='lte', name='total', label='Total(To)')
	date__gte = django_filters.DateTimeFilter(lookup_expr='gte', name='date', label='Date(From)', 
							widget=DateWidget(attrs={'id':"date__gte"}, 
									bootstrap_version=3, options = dateTimeOptions))
	
	date__lte = django_filters.DateTimeFilter(lookup_expr='lte', name='date', label='Date(To)',
							widget=DateWidget(attrs={'id':"date__lte"}, 
													bootstrap_version=3, options = dateTimeOptions))

	class Meta:
		model = Bill
		fields = ['bill_no', 'items__product__name','store'] 