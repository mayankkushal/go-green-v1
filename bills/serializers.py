from rest_framework import serializers
from bills.models import Bill, Item
from store.models import Product


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = ('product_name','sku', 'quantity', 'price', 'tax', 'total')

class BillSerializer(serializers.ModelSerializer):
	"""
	Serializes the bills instance for display and post
	"""
	store_name = serializers.ReadOnlyField()
	customer_name = serializers.ReadOnlyField()
	items = ItemSerializer(many=True)
	
	class Meta:
		model = Bill
		depth = 1
		fields = ('bill_no', 'store_name', 'date', 'customer_name', 'customer_no','items', 'original')
	

	def create(self, validated_data):
		"""
		Individually takes the `item` json and saves the instance
		"""
		items_data = validated_data.pop('items')
		bill = Bill.objects.create(**validated_data)
		for item_data in items_data:
			product = Product.objects.get(sku=item_data['sku'])
			Item.objects.create(bill=bill, product=product, **item_data)
		return bill


	
