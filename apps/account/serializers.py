from rest_framework import serializers
from .models import Account
from system.models import Role
from django.contrib.auth.hashers import make_password


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    status = serializers.BooleanField()
    description = serializers.CharField()
    # fields = ['id', 'name', 'status', 'description']


class AccountSerializer(serializers.Serializer):
    # class Meta:
    #     model = Account
    #     fields = '__all__'

    # password = serializers.CharField(max_length=100)
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        qs = obj.role.all()
        serializer = RoleSerializer(instance=qs, many=True)
        return serializer.data

    def create(self, validated_data):
        password = validated_data['password']
        validated_data['password'] = make_password(password, None, "pbkdf2_sha256")
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data['password']
        instance.email = validated_data['email']
        instance.password = make_password(password, None, "pbkdf2_sha256")
        instance.save()
        return instance

    # def validate_email(self, value):
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     if not (re.search(regex,value)): 
    #         raise serializers.ValidationError('Email is not valid.')