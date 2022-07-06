from collections import OrderedDict

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from utils.myPagenation import MyPageNumberPagination
from .models import Process
from account.models import Account
from .serializers import ProcessSerializer
from rest_framework.response import Response
from utils.webservice import TriggerProcess
from rest_framework.generics import ListAPIView

# Create your views here.


# class ProcessViewSet(ModelViewSet):
#     queryset = Process.objects.all()
#     serializer_class = ProcessSerializer


class ProcessAPIView(APIView):

    def get(self, request):
        queryset = Process.objects.all()
        # serializer = ProcessSerializer(instance=queryset, many=True)
        # return Response(serializer)
        qs = MyPageNumberPagination(queryset, request).GetPaginationQueryset()
        serializer = ProcessSerializer(instance=qs, many=True)
        data = OrderedDict([
            ('code', 1000),
            ('msg', '访问成功'),
            ('count', len(qs)),
            ('data', serializer.data)
        ])
        return Response(data)

    def post(self, request):
        data = request.data
        result = {'code': 1000, 'msg': None}
        serializer = ProcessSerializer(data=data)
        process = Process.objects.filter(processName=data['processName'])
        if process:
            result['code'] = 2001
            result['msg'] = '该process已经存在，无法添加'
            result['processName'] = data['processName']
            return Response(result)
        if serializer.is_valid(raise_exception=True):
            user = Account.objects.filter(email=data['owner']).first()
            if not user:
                result['code'] = 2002
                result['msg'] = 'Process owner没有注册'
            else:
                serializer.save(owner=data['owner'])
                result['msg'] = 'Process添加成功'
                result['processName'] = data['processName']
                result = dict(result, **serializer.data)
            return Response(result)


class ProcessDetailAPIView(APIView):

    def get(self, request, pk):
        data = request.data
        queryset = Process.objects.filter(pk=pk).first()
        serializer = ProcessSerializer(instance=queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        result = {'code': 1000, 'msg': None}
        process = Process.objects.filter(pk=pk).first()
        if not process:
            result['code'] = 2003
            result['msg'] = '该Process不存在，无法修改'
            result['processName'] = data['processName']
            return Response(result)
        serializer = ProcessSerializer(instance=process, data=data)
        serializer.save(owner=data['owner'])
        result['msg'] = '修改成功'
        result = dict(result, **serializer.data)
        return Response(result)

    def delete(self, request, pk):
        data = request.data
        result = {'code': 1000, 'msg': None}
        process = Process.objects.filter(pk=pk).first()
        if not process:
            result['code'] = 2004
            result['msg'] = '该Process不存在，无法删除'
            result['processName'] = data['processName']
            return Response(result)
        serializer = ProcessSerializer(instance=process, data=data)
        if serializer.is_valid(raise_exception=True):
            process.delete()


class ProcessTriggerAPIView(APIView):

    def post(self, request, pk):
        data = request.data
        result = {'code': 1000, 'msg': None}
        process = Process.objects.filter(pk=pk).first()
        if not process:
            result['code'] = 2005
            result['msg'] = "该Process不存在，无法trigger"
            result['processName'] = data['processName']
            return Response(result)
        serializer = ProcessSerializer(instance=process, data=data)
        if serializer.is_valid(raise_exception=True):
            isSameRecord = self.ValidateParams(serializer.data, data)
            if not isSameRecord:
                result['code'] = 2006
                result['msg'] = "请确认请求参数正确之后再发送请求"
                result['processName'] = data['processName']
                result['postBody'] = data['postBody']
                result['functionName'] = data['functionName']
                result['owner'] = data['owner']
                return Response(result)
            else:
                server = '137.182.193.146:8181'
                functionName = 'zkktest'
                postBody = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/"><Body><zkktest ' \
                           'xmlns="urn:blueprism:webservice:zkktest"/></Body></Envelope> '
                # TriggerProcess(server, functionName, postBody)
                result['msg'] = 'Process trigger成功'
                result['processName'] = data['processName']
                return Response(result)
        pass

    def ValidateParams(self, serializerData, data):
        isSameRecord = False
        keyList = ['processName', 'postBody', 'functionName', 'owner']
        for key in data.keys():
            if key not in keyList:
                data.pop(key)
        if serializerData == data:
            isSameRecord = True
        return isSameRecord

