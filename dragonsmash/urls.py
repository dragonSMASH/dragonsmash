from django.conf.urls import include, url
from api import urls as api_urls

urlpatterns = [
    url(r'^api/v1/', include(api_urls)),
]
