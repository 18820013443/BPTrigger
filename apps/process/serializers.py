from rest_framework import serializers
from .models import Process
from account.models import Account


class ProcessSerializer(serializers.Serializer):
    # class Meta:
    #     model = Process
    #     fields = '__all__'
    id = serializers.IntegerField()
    processName = serializers.CharField(max_length=1000)
    postBody = serializers.CharField()
    functionName = serializers.CharField(max_length=3000)
    owner = serializers.SerializerMethodField()

    def get_owner(self, row):
        email = row.owner.email
        return email

    def update(self, instance, validated_data):
        instance.processName = validated_data['processName']
        instance.postBody = validated_data['postBody']
        instance.functionName = validated_data['functionName']
        user = Account.objects.get(email=validated_data['owner'])
        instance.owner = user
        instance.save()
        return instance

    def create(self, validated_data):
        user = Account.objects.get(email=validated_data['owner'])
        processName = validated_data['processName']
        postBody = validated_data['postBody']
        functionName = validated_data['functionName']
        return Process.objects.create(processName=processName, postBody=postBody, functionName=functionName, owner=user)
