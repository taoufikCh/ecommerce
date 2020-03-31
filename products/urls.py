
from django.urls import path, re_path
from django.conf.urls import url
from .views import (
	ProductListView, 
	# product_list_view, 
	# product_detail_view, 
	# ProductDetailView,
	# ProductFeaturedListView,
	# ProductFeaturedDetailView,
	ProductDetailSlugView
	)

app_name = 'products'
urlpatterns = [

	path('', ProductListView.as_view(), name='list'),
	re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
]
