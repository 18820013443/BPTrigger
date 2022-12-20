from django.urls import path, re_path
from .views import MenusBuildAPIView, MenusAPIView, RoleAPIView, TreeDataView

urlpatterns = [
    re_path(r'menus/build/$', MenusBuildAPIView.as_view()),
    re_path(r'menus/$', MenusAPIView.as_view()),
    re_path(r'role/$', RoleAPIView.as_view()),
    re_path(r'menus/tree/$', TreeDataView.as_view())
]
