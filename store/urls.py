from django.conf.urls import url,include
from django.views.generic import DetailView, TemplateView, ListView
from django.views.decorators.csrf import csrf_exempt


from . import views
from .models import Store


app_name = "store"
urlpatterns = [
	url(r'^create_store/$', views.StoreCreate.as_view(), name='store_add'),
	url(r'^store_update/(?P<slug>[\w\-]+)/$', views.StoreUpdate.as_view(), name="store_update"),
	url(r'^detail/(?P<slug>[\w\-]+)$', DetailView.as_view(
		context_object_name="store", 
		model=Store
		), name="store_detail"),
	url(r'^store_list', ListView.as_view(
		context_object_name='store_list',
		model=Store
		), name="store_list"),
	
	url(r'^locator', views.StoreLocator.as_view(), name='locator'),
	
	url(r'^add_product', views.ProductCreate.as_view(), name="add_product"),
	url(r'^update_product/(?P<pk>[\w\-]+)/', views.ProductUpdate.as_view(), name="update_product"),
	url(r'^product_list', views.ProductListView.as_view(), name='product_list'),
	url(r'^(?P<pk>[\w\-]+)/delete', views.ProductDelete.as_view(), name='delete_product')
]