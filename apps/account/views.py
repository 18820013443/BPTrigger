from django.shortcuts import render
from .serializers import AccountSerializer
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Account
from rest_framework.response import Response


# Create your views here.


class AccountViewSet(APIView):
    # queryset = Account.objects.all()
    # serializer_class = AccountSerializer
    def get(self, request):
        queryset = Account.objects.all()
        serializer = AccountSerializer(instance=queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            pass
        pass

    def put(self, request):
        pass


    def delete(self, request):
        pass

    


        

    pass




