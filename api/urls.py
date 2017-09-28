from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	url(r'^login/(?P<username>[\w\-]+)/(?P<password>[\w\-]+)', views.get_user_token),
	url(r'^client_bill_list/', views.ClientBillList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns) 