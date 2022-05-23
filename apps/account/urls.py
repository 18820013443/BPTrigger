from django.urls import path, include

from django.urls import re_path, include
from rest_framework import routers
from .views import AccountViewSet

router = routers.SimpleRouter()
router.register(r'account', AccountViewSet)
urlpatterns = router.urls
