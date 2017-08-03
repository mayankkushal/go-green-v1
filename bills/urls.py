from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from bills import views

urlpatterns = [
	url(r'^api$', views.BillList.as_view()),
	url(r'^api/(?P<bill_no>[0-9]+)$', views.BillDetail.as_view()),
	url(r'^list$', views.BillListView.as_view(), name='bill_list'),
	url(r'^detail/(?P<pk>[\w\-]+)$', views.BillDetailView.as_view(), name="bill_detail"),
	url(r'^check_notified', views.check_notification)
]

urlpatterns = format_suffix_patterns(urlpatterns) 