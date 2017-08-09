from django.conf.urls import url,include
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.decorators import login_required

from . import views
from .models import Profile

urlpatterns = [
	
	url(r'^user/profile_create/', views.ProfileCreate.as_view(), name="profile_add"),
	url(r'^user/profile_update/(?P<pk>[\w\-]+)', views.ProfileUpdate.as_view(), name="profile_update"),
	url(r'^user/profile/(?P<slug>[\w\-]+)', login_required(views.ProfileDetailView.as_view()), name="profile-view"),

	url(r'^newsletter', views.newsletter, name='newsletter'),
	url(r'^download_email', views.download_email),
	
	url(r'^verify', views.OTPVerificationView.as_view(), name='otp-verify'),
	url(r'^clear_pin', views.clear_pin),
	url(r'^resend_otp', views.resend_otp),
	url(r'^inactive_otp', views.inactive_otp, name='inactive_otp'),
	
	url(r'^login_redirect', views.profile_login, name="profile_login"),
	url(r'^password_change/$', views.change_password, name='change_password'),
		
	url(r'^qr_scanner', views.qr_scanner, name="qr_scanner"),
	url(r'^qr_redirect', views.QrRedirect.as_view(), name='qr_redirect'),
	
	url(r'^notify', views.NotificationView.as_view(), name='notify'),
	url(r'^mark_read', views.mark_read),
		
	url(r'^$', views.HomePage.as_view(), name="index"),
]