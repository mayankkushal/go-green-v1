from django.shortcuts import render, reverse
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Min
from django.utils.decorators import method_decorator
from easy_pdf.views import PDFTemplateResponseMixin

import json
import datetime

from client.models import Profile
from store.models import Store

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from bills.models import Bill
from .serializers import BillSerializer
from django.contrib.auth.models import User
from .filters import BillFilter

# Create your views here.

class BillList(APIView):
	"""
	List all Bills, or Create new Bill for the API
	"""

	def get(self, request, format=None):
		bills = Bill.objects.all()
		serializer = BillSerializer(bills, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = BillSerializer(data=request.data)
		if serializer.is_valid():
			customer = User.objects.get(profile__phone_no=request.data['customer_no'])
			serializer.save(store=request.user.store, customer=customer)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, Update or Destroy the Bill instance API
	"""
	queryset = Bill.objects.all()
	serializer_class = BillSerializer


@method_decorator(login_required, name='dispatch')
class BillListView(ListView):
	"""
	Lists the bills for the respective users
	"""

	model = Bill
	paginate_by = 15
	
	def get_context_data(self, **kwargs):
		"""
		Returns the bills queryset if the the profile is available.
		Adds a filter, and passes all the required data for jquery plugin.
		"""
		context = super(BillListView, self).get_context_data(**kwargs)
		bill_filter_qs = []
		bill_filter = []

		if Profile.objects.filter(user=self.request.user).exists():
			customer_no = self.request.user.profile.phone_no.national_number
			bill_list = Bill.objects.filter(customer_no=customer_no)
			bill_filter = BillFilter(self.request.GET, queryset=bill_list)
			
			bill_filter.dateTimeOptions['startDate'] = self.request.user.date_joined.date().strftime("%m-%d-%Y")
			bill_filter.dateTimeOptions['endDate'] = datetime.date.today().strftime("%m-%d-%Y")
			if bill_list:
				context['total_min'] = int(Bill.objects.filter(customer_no=customer_no).aggregate(Min('total'))['total__min'])
				context['total_max'] = int(Bill.objects.filter(customer_no=customer_no).aggregate(Max('total'))['total__max'])

			bill_filter_qs = BillFilter(self.request.GET, queryset=bill_list).qs
			
			paginator = Paginator(bill_filter_qs, self.paginate_by)

		elif Store.objects.filter(user=self.request.user).exists():
			"""
			If the user is store return a list of bills from the list of `pk` taken from session
			"""
			return_bill_list = []
			bill_pk = self.request.session.get('bill_pk')
			for pk in bill_pk:
				try:
					return_bill_list.append(Bill.objects.get(pk=str(pk), editable=True))
				except Bill.DoesNotExist:
					pass
			self.request.session['bill_pk'] = []

			paginator = Paginator(return_bill_list, self.paginate_by)

		page = self.request.GET.get('page')
		try:
			bills = paginator.page(page)
		except PageNotAnInteger:
			bills = paginator.page(1)
		except EmptyPage:
			bills = paginator.page(paginator.num_pages)

		context['bill_list'] = bills
		context['filter'] = bill_filter
				
		return context


@method_decorator(login_required, name='dispatch')
class BillDetailView(UserPassesTestMixin, DetailView):
	"""
	Individual bill details
	"""

	model = Bill
	context_object_name = 'bill' 

	def test_func(self):
		"""
		Only allows the customer and the store of the bill to access the details
		"""
		bill = self.get_object()
		customer = User.objects.get(profile__phone_no=bill.customer_no)
		if (self.request.user == customer) or (self.request.user.store == bill.store):
			return self.request.user
		else:
			return None

	def get_context_data(self, **kwargs):
		'''
			1) Checks if the user is coming from the notifications page.
			2) If the user is coming from the notifications page, check the
				`pk` of the current bill with the bills in the unread notifications.
				a) If they match makrk the notification read
			3) Return the context	
		'''
		context = super(BillDetailView, self).get_context_data(**kwargs)
		
		# URL of the previos page
		referer = self.request.META.get('HTTP_REFERER') 
		# URL of the notifications page (/notify)
		notify= self.request.build_absolute_uri(reverse('notify'))
		
		if referer == notify:	# Check if they are same
			notifications = self.request.user.notifications.unread()
			for n in notifications:
				try:
					if str(n.data['pk']) == self.kwargs['pk']:
						n.mark_as_read()
						break 
				except:
					pass
		
		return context


@login_required
def check_notification(request):
	"""
	Checks if `notified` is still false in the bill and sends push notification
	and changes `notified` to true
	"""
	try:
		un_notified = Bill.objects.filter(customer=request.user, notified=False)[0]
	except:
		un_notified = None
	if un_notified:
		un_notified.notified = True
		un_notified.save()
		red_url = '/bills/detail/'+str(un_notified.pk)
		bill_detail = {"store":un_notified.store_name, "customer":un_notified.customer_name, "url":red_url }
		return HttpResponse(json.dumps(bill_detail), content_type='application/json')
	return HttpResponse("All notified")
	

class BillPDFView(PDFTemplateResponseMixin, DetailView):
	model = Bill
	template_name = 'bills/bill_pdf.html'
	context_object_name = 'bill'

	def get_context_data(self, **kwargs):
		context = super(BillPDFView, self).get_context_data(**kwargs)
		context['user'] = self.request.user.is_authenticated()
		bill = self.get_object()
		try:
			customer = Profile.objects.get(phone_no=bill.customer_no)
		except:
			customer = None
		context['customer'] = customer
		return context