from django.urls import path, re_path
from django.conf.urls import url
from .views import (
	cart_home, 
	cart_update,
	checkout_home,
	checkout_done_view
	)

app_name = 'products'
urlpatterns = [

	path('', cart_home, name='home'),
	# re_path(r'^(?P<slug>[\w-]+)/$', cart_update.as_view(), name='detail'),
	url(r'^checkout/success/$', checkout_done_view, name='success'),
	url(r'^checkout/$', checkout_home, name='checkout'),
	url(r'^update/$', cart_update, name='update'),
]
