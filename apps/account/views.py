from django.shortcuts import render
from .serializers import AccountSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Account


# Create your views here.


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer




