from rest_framework import serializers
from .models import Process
from account.models import Account


class ProcessSerializer(serializers.Serializer):
    # class Meta:
    #     model = Process
    #     fields = '__all__'

    processName = serializers.CharField(max_length=1000)
    postBody = serializers.CharField()
    owner = serializers.SerializerMethodField()

    def get_owner(self, row):
        owner = row.account.email
