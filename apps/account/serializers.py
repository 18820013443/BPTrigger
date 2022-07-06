import email
from enum import unique
from rest_framework import serializers
from .models import Account
from django.conf import settings
import re
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.Serializer):
    # class Meta:
    #     model = Account
    #     fields = '__all__'

    # password = serializers.CharField(max_length=100)
    id = serializers.IntegerField(required=False)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField()

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