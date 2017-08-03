from django import forms
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from phonenumber_field.formfields import PhoneNumberField
from datetimewidget.widgets import DateWidget

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['profile_pic', 'first_name', 'last_name', 'dob', 'gender', 'address']
		widgets = {
			'dob':DateWidget(attrs={'id':"id_dob"}, bootstrap_version=3, options ={'format': 'mm/dd/yyyy'} )
		}

from registration.forms import RegistrationForm
class RegisterProfileForm(RegistrationForm):
	'''
	Adds phone number to the registration form 
	'''
	phone_no = PhoneNumberField(widget=PhoneNumberInternationalFallbackWidget)

	def clean(self):
		try:
			if Profile.objects.filter(phone_no=self.cleaned_data['phone_no']).exists():
				raise forms.ValidationError("Phone Number already exists!")
		except KeyError:
			pass

		return self.cleaned_data


from django.core.cache import cache
import random
import requests
def user_created(sender, user, request, **kwargs):
	'''
	Saves the phone number to the profile and sets the user `is_active = False`
	`is_active` only set true if verified by sms

	'''
	form = RegisterProfileForm(request.POST)
	data = Profile(user=user)
	user.is_active = False
	user.save()
	phone_no = form.data['phone_no']

	length = 6 # No of digits of code
	pin = random.sample(range(10**(length-1), 10**length), 1)[0]
	request.session['cur_number'] = phone_no
	request.session[str(phone_no)] =  pin

	#Sending code goes here
	print("Your otp is "+ str(request.session[phone_no])) 
	request.session['otp'] = pin
	
	data.phone_no = phone_no
	data.save()

from registration.signals import user_registered
user_registered.connect(user_created)


class OTPVerificationForm(forms.Form):
	'''
	OTP form, for pin and phone number
	'''
	pin = forms.CharField(max_length=5)
