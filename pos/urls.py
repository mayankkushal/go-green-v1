from django.conf.urls import url,include

from . import views

urlpatterns = [
	url(r'^billing', views.CreateBill.as_view(), name='billing'),
	url(r'^return/(?P<pk>[\w\-]+)$', views.ReturnBill.as_view(), name='return_bill'),
	url(r'^product_autocomplete', views.ProductAutocomplete.as_view(), name="product_autocomplete"),
	url(r'^sku_autocomplete', views.SKUAutocomplete.as_view(), name="sku_autocomplete"),
	url(r'^product_detail', views.product_detail, name="product_detail")
]