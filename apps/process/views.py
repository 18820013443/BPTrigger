from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Process
from .serializers import ProcessSerializer
# Create your views here.


class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
