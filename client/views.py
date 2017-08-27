from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic import DetailView, TemplateView, RedirectView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin

import json
import csv
import random
import re
import datetime
import twitter
import pytz
 
from .models import Profile, SlideShowImage, Banner, Newsletter
from .forms import ProfileUpdateForm, OTPVerificationForm
from bills.models import Bill
from blog.models import Article
from store.models import Store
from django.contrib.auth.models import User

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

class HomePage(TemplateView):
	template_name='client/index.html'

	def get_tweets(self):
		"""
		returns twitter feed with settings as described below, contains all related twitter settings
		"""
		api = twitter.Api(consumer_key=settings.TWITTER_FEED_CONSUMER_PUBLIC_KEY,
						  consumer_secret=settings.TWITTER_FEED_CONSUMER_SECRET,
						  access_token_key=settings.TWITTER_FEED_OPEN_AUTH_TOKEN,
						  access_token_secret=settings.TWITTER_FEED_OPEN_AUTH_SECRET
						  )

		return api.GetUserTimeline(screen_name='mob_bills', exclude_replies=True, include_rts=False) 

	def get_context_data(self, **kwargs):
		context = super(HomePage, self).get_context_data(**kwargs)
		banner = Banner.objects.get(name='HomepageSlider')
		slider_image = SlideShowImage.objects.filter(slideshow=banner)
		context['slider_image'] = slider_image

		article_list = Article.objects.filter().order_by('-date_created')[:3]
		context['article_list'] = article_list
		context['tweets'] = self.get_tweets()
		
		return context



class ProfileCreate(CreateView):
	form_class = ProfileUpdateForm 
	model = Profile

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ProfileCreate, self).form_valid(form)

	def form_invalid(self, form):
		return HttpResponse("There was some error. Please try again later")



class ProfileUpdate(UpdateView):
	form_class = ProfileUpdateForm
	model = Profile
	context_object_name = 'profile'



class ProfileDetailView(DetailView):
	model = Profile
	context_object_name = 'cur_user'
	slug_field = 'phone_no'

	def get_context_data(self, **kwargs):
		context = super(ProfileDetailView, self).get_context_data(**kwargs)
		return context



@login_required
def profile_login(request):
	"""
	On user login method redirects the user according to thier status
	1)If the user is active, ie. has verified phone number
		a) client - redirected to bills page
		b) store - redirected to `billing_start.html` page
		c) admin - redirected to admin page
	2)If the user is inactive ie. not verifeid redirect to the OTP verification
		page.

	"""
	if request.user.is_active:
		if request.user.is_superuser:
			return redirect("/green_admin/")

		else:
			try:
				profile = request.user.profile
				return redirect(reverse('bill_list'))
			except:
				slug = request.user.store.slug
				return redirect(reverse('qr_scanner'))
	else:
		return redirect('/inactive_otp')


def qr_scanner(request):
	return render(request, 'extra/qr_scanner.html')


class QrScannerReturn(UserPassesTestMixin, TemplateView):
	template_name = 'extra/qr_scanner_return.html'

	def test_func(self):
		try:
			store = self.request.user.store
		except:
			store = None
		return store


from registration.backends.simple.views import RegistrationView
class MyRegistrationView(RegistrationView):
	"""
	Overrides the success url to go to `verify` page
	"""

	def get_success_url(self, user):
		return "/verify"



class OTPVerificationView(FormView):
	'''
	Gets OTP and phone number from the page and matches with
	the pin stored in the session with that phone number as key.
	If matches, sets `user.is_active = True` else gives error message
	and prompts for resending the OTp
	'''
	template_name = 'client/otp_verify.html'
	form_class = OTPVerificationForm
	success_url = '/bills/list'
	pin = 0

	def verify_pin(self, pin, phone_no):
		try:
			return pin == str(self.request.session[phone_no])
		except KeyError:	# Since the key is deleted when time is up
			return False	

	def form_valid(self, form):
		
		pin = self.request.POST['pin']
		phone_no = self.request.session['cur_number']
		
		try:
			profile = Profile.objects.get(phone_no=phone_no)
		except MultipleObjectsReturned:
			profile = None
		
		if self.verify_pin(pin, phone_no) and profile:
			profile = Profile.objects.get(phone_no=phone_no)
			profile.user.is_active = True
			profile.user.save()
		else:
			return HttpResponse("Incorrect OTP, Please try again <a href='/resend_otp'>Verify</a>")
		return super(OTPVerificationView, self).form_valid(form)

	def get_context_data(self, **kwargs):

		context = super(OTPVerificationView, self).get_context_data(**kwargs)

		number = str(self.request.session['cur_number'])
		cur_number = ""
		for i in range(10):
			if i > 1 and i < 8:
				cur_number += '*'
				continue
			cur_number += number[i]

		context['cur_number'] = cur_number # Number with stars eg. 98******21, to display to which number OTP is sent
		context['otp'] = self.request.session['otp']
		return context


def clear_pin(request):
	'''
	Deletes the pin when the timer is up
	'''
	phone_no = request.session['cur_number']
	
	del request.session[phone_no]
	request.session.modified = True
	
	return HttpResponse()



def resend_otp(request):
	'''
	Resends a new OTP when 
		1) Incorrect OTP from user
		2) Clicking on `resend` button in verify.html page
	'''
	length = 6 # No of digits of code
	pin = random.sample(range(10**(length-1), 10**length), 1)[0]
	request.session[request.session['cur_number']] = pin

	#code to send OTP message goes HERE
	print("Your OTP is "+str(pin))
	request.session['otp'] = pin

	return redirect('/verify')



def inactive_otp(request):
	'''
		Sends an otp to the inactive user and redirects to the `verify` page
	'''
	request.session['cur_number'] = str(request.user.profile.phone_no.national_number)
	print(request.user.profile.phone_no.national_number)
	resend_otp(request)
	return redirect('/verify')



class NotificationView(TemplateView):
	"""
		View to render the notifications
	"""
	template_name = "client/notification.html"
	paginate_by = 20

	def get_context_data(self, **kwargs):
		context = super(NotificationView, self).get_context_data(**kwargs)

		notices = self.request.user.notifications.all()
		
		paginator = Paginator(notices, self.paginate_by)

		page = self.request.GET.get('page')
		try:
			notices = paginator.page(page)
		except PageNotAnInteger:
			notices = paginator.page(1)
		except EmptyPage:
			notices = paginator.page(paginator.num_pages)

		context['notices'] = notices

		return context



def mark_read(request):
	'''
		Mark all the unread notifications of the user read
	'''
	n = request.user.notifications.unread()
	n.mark_all_as_read()

	return redirect(reverse('notify'))



def change_password(request):
	"""
		Simple change password where old password is asked and if valid 
		new password can be entered
	"""
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'extra/change_password.html', {
		'form': form
	})


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



class QrRedirect(VerificationMixin, FormView):
	"""
	Redirects using the value from the qr code on `get` request and uses the
	values from the phone_no field for the `post` request.
	"""
	def get(self, request, *args, **kwargs):
		if self.is_customer():
			phone_no = request.GET['val']
			store = self.store_present(phone_no)
			if store:
				return redirect('/store/detail/'+store.slug)

		elif self.is_store():
			val = request.GET['val']
			
			if self.is_phone(val):
				phone_no = self.extract_value(val)
				if self.redirect_to_billing(phone_no):
					return redirect(reverse('billing'))

			elif self.is_bill(val):
				bill_pk = self.extract_value(val)
				bill = self.bill_present(bill_pk)
				if bill:
					if self.is_bill_return_valid(bill):
						return redirect('/pos/return/'+str(bill.pk))
					else:
						return redirect(reverse('qr_scanner'))

	def post(self, request, *args, **kwargs):
		if self.is_customer():
			num = request.POST.get('phone_no')
			store = self.store_present(num)
			if store:
				return redirect('/store/detail/'+store.slug)

		elif self.is_store():
			num = request.POST.get('phone_no')		
			self.request.session['cus_no'] = num
			return redirect(reverse('billing'))


class QRRedirectReturn(UserPassesTestMixin, VerificationMixin, FormView):
	"""
	Redirects using the value from the qr code on `get` request and uses the
	values from the phone_no field for the `post` request for returns.
	"""
	def test_func(self):
		try:
			store = self.request.user.store
		except:
			store = None
		return store

	def bill_to_list(self, phone_no):
		bill_pk = []
		bill = Bill.objects.filter(customer_no=phone_no)
		for b in bill:
			if b.return_valid:
				bill_pk.append(b.pk)
		return bill_pk

	def get(self, request, *args, **kwargs):
		if self.is_store():
			val = request.GET['val']
			
			if self.is_phone(val):
				phone_no = self.extract_value(val)
				bill_pk = self.bill_to_list(phone_no)
				self.request.session['bill_pk'] = bill_pk

				return redirect(reverse('bill_list'))

			elif self.is_bill(val):
				bill_pk = self.extract_value(val)
				bill = self.bill_present(bill_pk)
				if bill:
					if self.is_bill_return_valid(bill):
						return redirect('/pos/return/'+str(bill.pk))
					else:
						return redirect(reverse('qr_scanner_return'))
	
	def post(self, request, *args, **kwargs):
		if self.is_store():
			num = request.POST.get('phone_no')
			bill_no = request.POST.get('bill_no')
			bill_pk = []
			if num:
				bill_pk = self.bill_to_list(num)
				
			elif bill_no:
				bills = Bill.objects.filter(bill_no=bill_no)

				if len(bills) == 1 :
					return redirect('/pos/return/'+str(bills[0].pk))
				else:
					for b in bills:
						bill_pk.append(b.pk)
			
			self.request.session['bill_pk'] = bill_pk
			return redirect(reverse('bill_list'))




from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class InactiveAuthenticationForm(AuthenticationForm):

	def confirm_login_allowed(self, user):
		"""
		Controls whether the given User may log in. This is a policy setting,
		independent of end-user authentication. This default behavior is to
		allow login by active users, and reject login by inactive users.

		If the given user cannot log in, this method should raise a
		``forms.ValidationError``.

		If the given user may log in, this method should return None.
		"""
		if not user.is_active:
			return None


def newsletter(request):
	""" Simple Newsletter.
	Takes the email, validates it and stores it in the Newsletter model
	"""

	msg = ""
	status = None
	if request.method == 'POST':
		
		email = request.POST.get('email')
		try:
			validate_email(email)			

		except ValidationError:
			data = {
				'msg': "Invalid email, Please enter a valid email",
				'status': False
			}
			return HttpResponse(json.dumps(data), content_type='application/json')
		
		if Newsletter.objects.filter(email=email).exists():
			data = {
			'msg': "Email already exists.",
			'status': False
		}
		else:
			Newsletter.objects.create(email=email)
			data = {
				'msg': "You have been subcribed.",
				'status': True
			}

		return HttpResponse(json.dumps(data), content_type='application/json')
		

def download_email(request):
	"""
		Renders all the emails of the `Newsletter` to a .csv file.
		Only admin is allowed to download.
	"""
	if request.user.is_superuser:
		email_list = Newsletter.objects.all()

		response =  HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment;filename=newsletter-emails.csv'

		writer = csv.writer(response)
		for email in email_list:
			writer.writerow([email.email])

		return response
	else:
		return redirect(reverse('index'))



class ClientStatement(TemplateView):
	template_name = "client/statement.html"

	def get_bill_total(self, bills):
		total = 0
		for b in bills:
			total += b.total
		return total

	def get_unique_stores(self, bills):
		stores = []
		for b in bills:
			stores.append(b.store.name)
		return len(list(set(stores)))

	def get_context_data(self, **kwargs):
		context = super(ClientStatement, self).get_context_data(**kwargs)

		utc=pytz.UTC
		
		today_date = utc.localize(datetime.datetime.today())
		
		month_start = utc.localize(datetime.datetime.today().replace(day=1))
		next_month_start = datetime.datetime.today().replace(month=today_date.month + 1, day=1)
		month_end = utc.localize(next_month_start - datetime.timedelta(days=1))

		year_start = utc.localize(datetime.datetime.today().replace(month=1, day=1)) 
		year_end = utc.localize(datetime.datetime.today().replace(month=12, day=31))
		
		customer_no = self.request.user.profile.phone_no.national_number
		
		daily_bill = Bill.objects.filter(customer_no=customer_no, date=today_date)
		monthly_bill = Bill.objects.filter(customer_no=customer_no, 
						date__gte=month_start,
						date__lte=month_end
						)
		yearly_bill = Bill.objects.filter(customer_no=customer_no, 
						date__gte=year_start,
						date__lte=year_end
						)

		context['daily_count'] = len(daily_bill)
		context['monthly_count'] = len(monthly_bill)
		context['yearly_count'] = len(yearly_bill)

		context['daily_total'] = self.get_bill_total(daily_bill)
		context['monthly_total'] = self.get_bill_total(monthly_bill)
		context['yearly_total'] = self.get_bill_total(yearly_bill)

		context['daily_store'] = self.get_unique_stores(daily_bill)
		context['monthly_store'] = self.get_unique_stores(monthly_bill)
		context['yearly_store'] = self.get_unique_stores(yearly_bill)

		return context