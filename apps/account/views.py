from collections import OrderedDict

from django.shortcuts import render
from .serializers import AccountSerializer
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Account
from rest_framework.response import Response
from account.utils.jwt_auth import create_token
from django.contrib.auth.hashers import check_password
from rest_framework.generics import ListAPIView
from utils.myPagenation import MyPageNumberPagination



# Create your views here.


class AccountAPIView(APIView):

    def get(self, request):
        queryset = Account.objects.all()
        result = {'code': 1000, 'msg': "访问成功"}
        # serializer = MyPageNumberPagination(queryset, request, AccountSerializer).GetPaginationQueryset()
        qs = MyPageNumberPagination(queryset, request).GetPaginationQueryset()
        serializer = AccountSerializer(instance=qs, many=True)
        data = OrderedDict([
            ('code', 1000),
            ('msg', '访问成功'),
            ('count', len(qs)),
            ('data', serializer.data)
        ])
        return Response(data)

    # 注册
    def post(self, request):
        data = request.data
        result = {'code': 1000, 'msg': None}
        serializer = AccountSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = Account.objects.filter(email=data['email']).first()
            if not user:
                # serializer.save(password=data['password'])
                serializer.save()
                # return Response(serializer.data)
            else:
                result['code'] = 1001
                result['msg'] = '该email已经存在'
                result['email'] = data['email']
                return Response(result)
        token = create_token({'email': data['email']})
        result['msg'] = "用户添加成功"
        result['email'] = serializer.data['email']
        result['token'] = token
        return Response(result)

class AccountDetailAPIView(APIView):

    def get(self, request, pk):
        queryset = Account.objects.filter(pk=pk).first()
        serializer = AccountSerializer(instance=queryset)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        result = {'code': 1000, 'msg': None}
        user = Account.objects.filter(pk=pk).first()
        serializer = AccountSerializer(instance=user, data=data)
        # user = Account.objects.filter(email=data['email'])
        if serializer.is_valid(raise_exception=True):
            if user:
                # serializer.save(password=data['password'])
                serializer.save()
                result['msg'] = "用户修改成功"
                result['email'] = serializer.data['email']
                result['password'] = serializer.data['password']
                return Response(result)
            else:
                result['code'] = 1002
                result['msg'] = '该用户不存在，无法修改'
                return Response(result)

    def delete(self, request, pk):
        data = request.data
        result = {'code': 1000, 'msg': None}
        user = Account.objects.filter(pk=pk).first()
        serializer = AccountSerializer(instance=user, data=data)
        if serializer.is_valid(raise_exception=True):
            if user:
                user.delete()
                result['msg'] = '用户删除成功'
            else:
                result['code'] = 1003
                result['msg'] = '该用户不存在，无法删除'
                return Response(result)


class AccountLoginView(APIView):

    def post(self, request):
        data = request.data
        data['email'] = request.data['username']
        result = {'code': 1000, 'msg': None}
        user = Account.objects.filter(email=data['email']).first()
        serializer = AccountSerializer(instance=user, data=data)
        if not user:
            result['code'] = 1004
            result['msg'] = "该用户不存在，请重新输入"
            return Response(result)
        if serializer.is_valid(raise_exception=True):
            if check_password(data['password'], user.password):
                result['msg'] = '登陆成功'
                token = create_token({'email': data['email']})
                result['email'] = user.email
                result['token'] = token
            else:
                result['code'] = 1005
                result['msg'] = '用户名或密码错误'
            return Response(result)


