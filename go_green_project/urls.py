"""go_green_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from client import views
import notifications.urls
from django.views.decorators.csrf import csrf_exempt
from client.forms import RegisterProfileForm
from django.contrib.sitemaps.views import sitemap

from django.contrib.auth import views as auth_views
import client.custom_authentication as custom_auth


from client.sitemaps import StoreSitemap, BlogSitemap, StaticSitemap, FlatPageSitemap

sitemaps = {
    'store': StoreSitemap(),
    'blog': BlogSitemap(),
    'static': StaticSitemap(),
    'info': FlatPageSitemap()
}


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^green_admin/', admin.site.urls),

    url(r'^accounts/register/$', views.MyRegistrationView.as_view(form_class=RegisterProfileForm), name='registration_register'),
    url(r'^login$', custom_auth.login , name='login'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^reset_otp', custom_auth.ResetOTPVerification.as_view(), name='reset_otp'),
    url(r'^password_reset_complete', custom_auth.ResetPasswordComplete.as_view(), name='reset_password_form'),
    url(r'^reset_password', custom_auth.ResetPasswordView.as_view(), name='reset_password'),


    
    url(r'^store/', include('store.urls')),
    url(r'^bills/', include('bills.urls')),
    url(r'^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^blog/', include('blog.urls')),
    url(r'^pos/', include('pos.urls')),
    url(r'^locator/', include('locator.urls', namespace='locator')),
    url(r'^', include('client.urls')),
    
    url(r'^info/', include('django.contrib.flatpages.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^robots\.txt$', include('robots.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


