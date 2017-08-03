from django.test import TestCase

from store.models import Store, Product
from client.tests import ProfileTest
# Create your tests here.

class StoreTest(TestCase):
	def create_store(self):
		u = ProfileTest().create_user('store', 'password')
		return Store.objects.create(store=u, 
			name='store name', 
			description='store description', 
			phone_no='7795206707', 
			address="store address"  )

	def test_store_creation(self):
		s = self.create_store()
		self.assertIsInstance(s, Store)
		self.assertEqual(s.__str__(), s.name)
		self.assertEqual(s.get_absolute_url(), '/store/detail/%s/' % s.slug)

class ProductTest(TestCase):

	def create_product(self):
		store = StoreTest().create_store()
		return Product.objects.create(store=store, name='product', sku='123456', price=265)

	def test_product_creation(self):
		p = self.create_product()
		self.assertIsInstance(p, Product)
		self.assertEqual(p.__str__(), 'product')
