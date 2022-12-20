from abc import ABC

from rest_framework import serializers
from .models import Menu


class MetaSerializer(serializers.Serializer):
    icon = serializers.CharField()
    title = serializers.CharField()


class SubMenuSerializer(serializers.Serializer):
    component = serializers.CharField()
    hidden = serializers.BooleanField()
    meta = serializers.SerializerMethodField()
    name = serializers.CharField()
    path = serializers.CharField()
    children = serializers.SerializerMethodField()

    def get_meta(self, obj):
        serializer = MetaSerializer(instance=obj)
        return serializer.data

    def get_children(self, obj):
        qs = Menu.objects.filter(parentId=obj.id)
        serializer = SubMenuSerializer(instance=qs, many=True)
        return serializer.data


class TopMenuSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    path = serializers.CharField()
    component = serializers.CharField()
    redirect = serializers.SerializerMethodField()
    name = serializers.CharField()
    meta = serializers.SerializerMethodField()
    hidden = serializers.BooleanField()
    alwaysShow = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    # meta = MetaSerializer(many=True)
    # title = serializers.CharField()
    # icon = serializers.CharField()
    # subCount = serializers.IntegerField()
    # menuSort = serializers.IntegerField()

    def get_alwaysShow(self, obj):
        # return False if obj.hidden else True
        return False

    def get_children(self, obj):
        qs = Menu.objects.filter(parentId=obj.id)
        for item in qs:
            self.get_children(item)
        serializer = SubMenuSerializer(instance=qs, many=True)
        return serializer.data

    def get_meta(self, obj):
        serializer = MetaSerializer(instance=obj)
        return serializer.data

    def get_redirect(self, obj):
        return 'noredirect'


class MenusSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    path = serializers.CharField()
    component = serializers.CharField()
    componentName = serializers.CharField(source='name')
    hidden = serializers.BooleanField()
    pid = serializers.SerializerMethodField()
    hasChildren = serializers.SerializerMethodField()
    icon = serializers.CharField()
    title = serializers.CharField()
    menuSort = serializers.IntegerField()
    subCount = serializers.IntegerField()

    def get_hasChildren(self, obj):
        return True if obj.subCount > 0 else False

    def get_pid(self, obj):
        return obj.name if obj.parentId is None else obj.parentId.name


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.BooleanField()
    description = serializers.CharField()
    menu = serializers.SerializerMethodField()

    def get_menu(self, obj):
        qs = obj.menu.all()
        serializer = MenusSerializer(instance=qs, many=True)
        return serializer.data


class TreeDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(source='name')
    children = serializers.SerializerMethodField()

    def get_children(self, obj):
        qs = Menu.objects.filter(parentId=obj.id)
        for item in qs:
            self.get_children(item)
        serializer = TreeDataSerializer(instance=qs, many=True)
        return serializer.data

