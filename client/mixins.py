import pytz
import datetime
import re

from .models import Profile, SlideShowImage, Banner, Newsletter
from .forms import ProfileUpdateForm, OTPVerificationForm
from bills.models import Bill
from blog.models import Article
from store.models import Store
from django.contrib.auth.models import User


class StatementMixin:
	"""
	Methods used in statements for both customer and store
	"""
	def get_bill_total(self, bills):
		"""
			Returns the sum of totals of all the bills
		"""
		total = 0
		for b in bills:
			if b.editable:
				total += b.total
		return total

	def get_unique_stores(self, bills):
		"""
			Returns the number of unique stores
		"""
		stores = []
		for b in bills:
			stores.append(b.store.name)
		return len(list(set(stores)))

	def get_unique_customers(self, bills):
		"""
			Returns the number of unique customers
		"""
		customers = []
		for b in bills:
			customers.append(b.customer_no)
		return len(list(set(customers)))

	def get_week_dates(self):
		week_start = pytz.timezone('Asia/Calcutta').localize(datetime.datetime.today()) - datetime.timedelta(days=datetime.datetime.today().weekday())
		week_end = week_start + datetime.timedelta(days=6)
		return week_start.replace(hour=00, minute=00), week_end.replace(hour=23, minute=59)

	def get_month_dates(self):
		month_start = pytz.timezone('Asia/Calcutta').localize(datetime.datetime.today().replace(day=1))
		next_month_start = datetime.datetime.today().replace(month=datetime.datetime.today().month + 1, day=1)
		month_end = pytz.timezone('Asia/Calcutta').localize(next_month_start - datetime.timedelta(days=1))
		return month_start.replace(hour=00, minute=00), month_end.replace(hour=23, minute=59)

	def get_year_dates(self):
		year_start = pytz.timezone('Asia/Calcutta').localize(datetime.datetime.today().replace(month=1, day=1)) 
		year_end = pytz.timezone('Asia/Calcutta').localize(datetime.datetime.today().replace(month=12, day=31))
		return year_start.replace(hour=00, minute=00), year_end.replace(hour=23, minute=59)

	def get_daily_bill(self, customer_no=None, store=None):
		today_date = pytz.timezone('Asia/Calcutta').localize(datetime.datetime.today())
		if customer_no:
			return Bill.objects.filter(customer_no=customer_no,
							date__gt=today_date - datetime.timedelta(days=1),
							date__lt=today_date + datetime.timedelta(days=1))
		else:
			return Bill.objects.filter(store=store,
							date__gt=today_date - datetime.timedelta(days=1),
							date__lt=today_date + datetime.timedelta(days=1))


	def get_bill_in_range(self, date_start, date_end, customer_no=None, store=None):
		"""
			Returns the bills in the certain range
		"""
		if customer_no:
			return Bill.objects.filter(customer_no=customer_no, 
							date__gte=date_start,
							date__lte=date_end,
							)
		else:
			return Bill.objects.filter(store=store, 
							date__gte=date_start,
							date__lte=date_end,
							)


class VerificationMixin:
	def is_customer(self):
		return True if Profile.objects.filter(user=self.request.user).exists() else False

	def is_store(self):
		return True if Store.objects.filter(user=self.request.user).exists() else False

	def store_present(self, slug):
		"""
			Checks if the store is present if not, raise a `404` 
		"""
		store = None
		try:
			store = Store.objects.get(phone_no=str(num))
		except Store.DoesNotExist:
			raise Http404()
		return store

	def customer_present(self, phone_no):
		"""
			Checks if the customer is present if not, raise a `404` 
		"""
		client = None
		try:
			client = User.objects.get(profile__phone_no=phone_no)
		except User.DoesNotExist:
			raise Http404()
		return client

	def bill_present(self, bill_pk):
		"""
			Checks if the bill is present if not, raise a `404` 
		"""
		bill = None
		try:
			bill = Bill.objects.get(pk=bill_pk)
		except:
			raise Http404()
		return bill

	def is_phone(self, val):
		"""
			The value from the qr is matched with `ph:` for phone number
		"""
		return bool(re.match(r'^ph:\d', val))

	def is_bill(self, val):
		"""
			The value from the qr is matched with `bi:` for bill number
		"""
		return bool(re.match(r'^bi:\d', val))
	
	def extract_value(self, val):
		"""
			Returns all the letters after the first 3 letters, ie leaving `ph:` or `bi:`
		"""
		return val[3:]

	def is_bill_return_valid(self, bill):
		"""
			Returns True if the bill is eligible to be returned.
			Conditions:
				a)Bill shouldn't be returned already ie. `bill.original` should be True
				b)Bill should lie in return period of that specific store.
		"""
		store = bill.store
		days_occured = datetime.date.today() - bill.date.date()
		if days_occured < datetime.timedelta(store.return_days):
			return True
		else:
			messages.error(self.request, 
				'Bill has crossed its return period. Store allows return within '+str(store.return_days)+" days")
			return False
		return False

	def redirect_to_billing(self, phone_no):
		client = self.customer_present(phone_no)
		if client:
			self.request.session['cus_no'] = client.profile.phone_no.national_number
			return True
