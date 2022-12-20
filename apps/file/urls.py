from django.urls import re_path
from .views import UploadFileAPIView, UploadFileDetailAPIView, QueryFilesAPIView, DownloadFileAPIView

urlpatterns = [
    re_path(r'query/$', QueryFilesAPIView.as_view()),
    re_path(r'upload/$', UploadFileAPIView.as_view()),
    re_path(r'delete/(?P<pk>\d+)/$', UploadFileDetailAPIView.as_view()),
    re_path(r'download/$', DownloadFileAPIView.as_view()),

]
