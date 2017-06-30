from django.conf.urls import url
from . import views

app_name = 'photos'

urlpatterns = [
	# /photos/
	url(r'^$', views.Index , name='index'),

	# /photos/<photo_id>
	url(r'^(?P<image_id>[0-9]+)$', views.detail,  name='detail'),

	#/photos/search-results/
	url(r'^search-results/$', views.search , name='search'),

	#/photos/<class_id>
	url(r'^(?P<id>[0-9]+)/$', views.search_buttons , name='search_buttons'),

	# /photos/
	url(r'^$', views.test ,  name='after_login_page'),


]
