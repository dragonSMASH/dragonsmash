from django.conf.urls import url
from views import status, register
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^status/', status, name="status"),
    url(r'auth/register', register, name="register"),
    url(r'auth/login', views.obtain_auth_token, name="register"),


]

