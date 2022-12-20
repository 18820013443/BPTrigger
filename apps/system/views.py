from django.shortcuts import render
from rest_framework.views import APIView
from .models import Menu, Role
from .serializers import TopMenuSerializer, MenusSerializer, RoleSerializer, TreeDataSerializer
from rest_framework.response import Response
from .filters import MenuFilter, RoleFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class MenusBuildAPIView(APIView):

    def get(self, request):
        qs = Menu.objects.filter(parentId=None)
        serializer = TopMenuSerializer(instance=qs, many=True)
        return Response(serializer.data)


class MenusAPIView(APIView):
    filterset_class = MenuFilter
    filter_backends = [DjangoFilterBackend]

    def GetFilterQueryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        qs = Menu.objects.all()
        qs = self.GetFilterQueryset(qs)
        serializer = MenusSerializer(instance=qs, many=True)
        return Response(serializer.data)


class RoleAPIView(APIView):
    filterset_class = RoleFilter
    filter_backends = [DjangoFilterBackend]

    def GetFilterQueryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get(self, request):
        qs = Role.objects.all()
        qs = self.GetFilterQueryset(qs)
        serializer = RoleSerializer(instance=qs, many=True)
        return Response(serializer.data)


class TreeDataView(APIView):

    def get(self, request):
        qs = Menu.objects.all()
        serializer = TreeDataSerializer(instance=qs, many=True)
        for item in serializer.data:
            self.DeleteBlankChildren(item)
        return Response(serializer.data)

    def DeleteBlankChildren(self, item):
        if item.children:
            self.DeleteBlankChildren(item)
