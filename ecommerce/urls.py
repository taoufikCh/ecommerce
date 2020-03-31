"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

# from products.views import (
# 	ProductListView, 
# 	product_list_view, 
# 	product_detail_view, 
# 	ProductDetailView,
# 	ProductFeaturedListView,
# 	ProductFeaturedDetailView,
# 	ProductDetailSlugView
# 	)

from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import checkout_address_create_view, checkout_address_reuse_view

from billing.views import payment_method_view, payment_method_createview
from carts.views import cart_detail_api_view
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView


from .views import home_page, about_page, contact_page

urlpatterns = [
	path('', home_page, name='home'),
	path('about/', about_page, name='about'),
	path('contact/', contact_page, name='contact'),
	re_path(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^checkout/address/create/$',checkout_address_create_view, name='checkout_address_create_view'),
	url(r'^checkout/address/reuse/$',checkout_address_reuse_view, name='checkout_address_reuse'),
	url(r'^register/guest/$', guest_register_view, name='guest_register'),
	path('logout/', LogoutView.as_view(), name='logout'),
	# path('cart/', cart_home, name='cart'),
	url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
	url(r'^cart/', include("carts.urls", namespace='cart')),
	url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
	url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
	url(r'^register/$', RegisterView.as_view(), name='register'),
	path('bootstrap/', TemplateView.as_view(template_name='bootstrap/exemple.html')),
	url(r'^products/', include("products.urls", namespace='products')),
	url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
	url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
	path('search/', include("search.urls", namespace='search')),
	# path('featured/', ProductFeaturedListView.as_view()),
	# re_path(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
	# path('products-fbv/', product_list_view),
	# #re_path(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
	# re_path(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
	# re_path(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)