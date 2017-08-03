from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.db.models import Q
from functools import reduce

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from store.models import Product, Store
from bills.models import Bill
from .forms import SearchForm
# Create your views here.

class SearchView(TemplateView):
	"""
	Processes the queries form the user and renders a result page
	"""
	form_class = SearchForm
	stores = []
	bills = []
	template_name = "extra/search_result.html"
	paginate_by = 4

	def query_list(self, query):
		"""
		Separates individual words from the query and removes unneccessary spaces, removes repeated words and 
		returns the query set
		"""
		return list(set(query.split()))

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		products =[]

		queries = self.query_list(request.GET['query'])
		
		products = Product.objects.filter(reduce(lambda x, y: x | y, [Q(name__icontains=q) for q in queries]))
		self.bills = list(set([Bill.objects.filter(items__product=p).order_by('-total')[0] for p in products]))

		return super(SearchView, self).get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):

		context = super(SearchView, self).get_context_data(**kwargs)

		paginator = Paginator(self.bills, self.paginate_by)

		page = self.request.GET.get('page')
		try:
			bill = paginator.page(page)
		except PageNotAnInteger:
			bill = paginator.page(1)
		except EmptyPage:
			bill = paginator.page(paginator.num_pages)

		context['bill_list'] = bill
		context['bill_count'] = len(self.bills)
		return context

