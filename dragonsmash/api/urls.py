from django.conf.urls import url
from rest_framework.authtoken import views
from .views import status, register, logout, location_update

urlpatterns = [
    url(r'^status/$', status, name="status"),
    url(r'^auth/register/$', register, name="register"),
    url(r'^auth/login/$', views.obtain_auth_token, name="login"),
    url(r'^auth/logout/$', logout, name="logout"),
    url(r'^player/location/$', location_update, name="location_update")
]
