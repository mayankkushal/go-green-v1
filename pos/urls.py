from django.conf.urls import url,include

from . import views

urlpatterns = [
	url(r'^billing_start', views.BillingStart.as_view(), name='billing_start'),
	url(r'^billing', views.CreateBill.as_view(), name='billing'),
	url(r'^product_autocomplete', views.ProductAutocomplete.as_view(), name="product_autocomplete"),
	url(r'^product_detail', views.product_detail, name="product_detail")
]