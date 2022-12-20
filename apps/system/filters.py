import django_filters
from .models import Menu, Role


class MenuFilter(django_filters.FilterSet):
    pid = django_filters.NumberFilter(field_name='parentId', lookup_expr='exact')

    class Meta:
        model = Menu
        fields = ['id', 'name', 'title']


class RoleFilter(django_filters.FilterSet):

    class Meta:
        model = Role
        fields = ['id', 'status', 'description']