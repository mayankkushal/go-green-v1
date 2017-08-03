from django.test import TestCase

from .models import Bill, Item as it
from client.tests import ProfileTest
from store.tests import StoreTest, ProductTest
# Create your tests here.

class BillTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.store = StoreTest().create_store()
		cls.customer = ProfileTest().create_user('customer', 'password')
		cls.b =  Bill.objects.create(store=cls.store, customer_no=cls.customer.id)

	def create_bill(self):
		return Bill.objects.create(store=self.store, customer_no=self.customer.id)

	def test_bill_creation(self):
		self.assertIsInstance(self.b, Bill)
		self.assertEqual(self.b.__str__(), self.b.bill_no)
		self.assertEqual(self.b.store_name, self.b.store.name)

class ItemTest(TestCase):
	def setUp(cls):
		cls.bill = BillTest().create_bill()
		cls.product = ProductTest().create_product()
	
	def create_item(self,q=4, bil=None):
		bil = self.bill
		return it.objects.create(bill=bil, product=self.product, quantity=q)

	def test_item_creation(self):
		i = self.create_item()
		self.assertIsInstance(i, it)
		self.assertEqual(i.__str__(), i.product.name)
		self.assertEqual(i.get_total(), i.product.price * i.quantity)



