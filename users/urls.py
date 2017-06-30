from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.generic import TemplateView

app_name = 'users'

urlpatterns = [
    url(r'^register/' , views.UserRegistration , name='register'),
    url(r'^login/' , views.LoginRequest , name='login'),
    url(r'^logout/' , views.LogoutRequest , name='logout'),




]



