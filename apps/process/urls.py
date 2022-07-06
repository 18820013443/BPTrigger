from django.urls import re_path, path
from rest_framework import routers
# from .views import ProcessViewSet
from .views import ProcessAPIView, ProcessDetailAPIView, ProcessTriggerAPIView

# router = routers.SimpleRouter()
# router.register(r'process', ProcessViewSet)
# urlpatterns = router.urls
urlpatterns = [
    re_path(r'^process/$', ProcessAPIView.as_view()),
    re_path(r'^process/(?P<pk>\d+)/$', ProcessDetailAPIView.as_view()),
    re_path(r'^process/trigger/(?P<pk>\d+)/', ProcessTriggerAPIView.as_view())
]
