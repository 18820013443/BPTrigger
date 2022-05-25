import email
from enum import unique
from rest_framework import serializers
from .models import Account
import re


class AccountSerializer(serializers.Serializer):
    # class Meta:
    #     model = Account
    #     fields = '__all__'

    # password = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.password = validated_data['password']
        return instance

    # def validate_email(self, value):
    #     regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    #     if not (re.search(regex,value)): 
    #         raise serializers.ValidationError('Email is not valid.')