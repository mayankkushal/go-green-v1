from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
	logout as auth_logout, update_session_auth_hash,
)
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages

import random

from .forms import PasswordResetForm, OTPVerificationForm
from .models import Profile



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


def _get_login_redirect_url(request, redirect_to):
	# Ensure the user-originating redirection URL is safe.
	if not is_safe_url(url=redirect_to, host=request.get_host()):
		return resolve_url(settings.LOGIN_REDIRECT_URL)
	return redirect_to



def login(request, template_name='registration/registration_form.html',
		  redirect_field_name=REDIRECT_FIELD_NAME,
		  authentication_form=InactiveAuthenticationForm,
		  extra_context=None, redirect_authenticated_user=False):
	"""
	Displays the login form and handles the login action.
	"""
	redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

	if redirect_authenticated_user and request.user.is_authenticated:
		redirect_to = _get_login_redirect_url(request, redirect_to)
		if redirect_to == request.path:
			raise ValueError(
				"Redirection loop for authenticated user detected. Check that "
				"your LOGIN_REDIRECT_URL doesn't point to a login page."
			)
		return HttpResponseRedirect(redirect_to)
	elif request.method == "POST":
		form = authentication_form(request, data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			return HttpResponseRedirect(_get_login_redirect_url(request, redirect_to))
	else:
		form = authentication_form(request)

	current_site = get_current_site(request)

	context = {
		'login_form': form,
		redirect_field_name: redirect_to,
		'site': current_site,
		'site_name': current_site.name,
	}
	if extra_context is not None:
		context.update(extra_context)

	return TemplateResponse(request, template_name, context)


class ResetPasswordView(FormView):
	template_name = "registration/reset_password.html"
	form_class = PasswordResetForm
	success_url = '/reset_otp'

	def generate_otp(self, phone_no):
		length = 6 # No of digits of code
		pin = random.sample(range(10**(length-1), 10**length), 1)[0]
		self.request.session[str(phone_no)] = pin
		self.request.session["otp"] = pin

	def form_valid(self, form):
		self.request.session['cur_number'] = form.cleaned_data['phone_no']
		self.generate_otp(form.cleaned_data['phone_no'])
		return HttpResponseRedirect(self.success_url)



class ResetOTPVerification(FormView):
	template_name = "registration/reset_password_confirm.html"
	form_class = OTPVerificationForm
	success_url = reverse_lazy('reset_password_form')
	login_url = reverse_lazy('login')

	def verify_pin(self, pin, phone_no):
		try:
			return pin == str(self.request.session[phone_no])
		except KeyError:	# Since the key is deleted when time is up
			return False

	def form_valid(self, form):
		pin = self.request.POST['pin']
		phone_no = self.request.session['cur_number']
		
		profile = Profile.objects.get(phone_no=phone_no)
		
		if self.verify_pin(pin, phone_no) and profile:
			return HttpResponseRedirect(self.get_success_url())

		else:
			messages.error(self.request, 'Incorrect OTP.')
			return HttpResponseRedirect(self.login_url)

	def get_context_data(self, **kwargs):

		context = super(ResetOTPVerification, self).get_context_data(**kwargs)

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


class ResetPasswordComplete(FormView):
	template_name = "registration/reset_password_form.html"
	form_class = SetPasswordForm
	success_url = success_url = '/bills/list'

	def get_form_kwargs(self, **kwargs):
		form_kwargs = super(ResetPasswordComplete, self).get_form_kwargs(**kwargs)
		user = User.objects.get(profile__phone_no=self.request.session['cur_number'])
		form_kwargs["user"] = user
		return form_kwargs

	def form_valid(self, form):
		form.save()
		return super(ResetPasswordComplete, self).form_valid(form)

