from django.urls import path, include

from django.urls import re_path, include
from rest_framework import routers
from .views import AccountAPIView, AccountDetailAPIView, AccountLoginView

# router = routers.SimpleRouter()
# router.register(r'account', AccountViewSet, basename='account')
# urlpatterns = router.urls

urlpatterns = [
    re_path(r'account/$', AccountAPIView.as_view()),
    re_path(r'account/(?P<pk>\d+)/$', AccountDetailAPIView.as_view()),
    re_path(r'account/login/$', AccountLoginView.as_view())
]
