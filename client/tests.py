from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User
# Create your tests here.
class ProfileTest(TestCase):

	def create_user(self, username, password):
		return User.objects.create(username=username, password=password)

	def create_profile(self):
		u = self.create_user('user', 'password')
		return Profile.objects.create(user=u, first_name='first', last_name='last', phone_no='7795206707', address="some address")

	def test_profile_creation(self):
		p = self.create_profile()
		self.assertTrue(isinstance(p, Profile))
		self.assertEqual(p.__str__(), p.first_name+" "+p.last_name)
		self.assertEqual(p.get_full_name, p.first_name+" "+p.last_name)
		self.assertEqual(p.get_absolute_url(), '/user/profile/%s/' % p.pk)