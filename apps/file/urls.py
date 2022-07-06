from django.urls import re_path
from .views import UploadFileAPIView, UploadFileDetailAPIView

urlpatterns = [
    re_path(r'upload/$', UploadFileAPIView.as_view()),
    re_path(r'delete/(?P<pk>\d+)/$', UploadFileDetailAPIView.as_view())
]
