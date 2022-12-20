import time
from collections import OrderedDict

from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from .serializers import UploadFileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from .models import File, Process
import os
from django.conf import settings
from rest_framework.decorators import api_view
# Create your views here.


def CheckFileUploadSuccessful(objFile, fileSize, waitTime):
    endTime = time.time() + waitTime
    while time.time() < endTime:
        if os.path.getsize(objFile.file.path) == fileSize:
            return True
    return False


class UploadFileAPIView(APIView):
    # parser_classes = [FileUploadParser]
    parser_classes = [MultiPartParser]

    def post(self, request):
        result, data = {'code': 1000, 'msg': None}, {}
        dataRequest = request.data
        objFile = dataRequest['file']
        fileSize = objFile.size
        fileName = objFile.name
        processId = dataRequest['processId']

        data['file'] = objFile
        data['fileName'] = fileName

        # 文件重名，修改文件名，修改传入数据库文件名
        filePath = os.path.join(settings.MEDIA_ROOT, 'InputFiles', fileName)
        if os.path.exists(filePath):
            strTime = time.strftime('%Y%m%d%H%M%S')
            (strFileName, strExtension) = os.path.splitext(fileName)
            fileName = f'{strFileName}_{strTime}{strExtension}'
            data['fileName'] = fileName
            objFile.name = fileName

        process = Process.objects.filter(id=processId).first()
        if not process:
            result['code'] = 3001
            result['msg'] = 'Process不存在！'
            return Response(result)
        data['process'] = processId
        serializer = UploadFileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if not ('.xls' in fileName or '.csv' in fileName):
                result['code'] = 3002
                result['msg'] = '文件必须为xlsx/xls/csv'
                return Response(result)
            instance = serializer.save()
            returnSerializer = UploadFileSerializer(instance=[instance], many=True)
            # isSaveSuccessful = CheckFileUploadSuccessful(instance, fileSize, 60)
            # if isSaveSuccessful:
            result['msg'] = f'{fileName}上传成功'
            data = OrderedDict([
                ('code', 1000),
                ('msg', f'{fileName}上传成功'),
                ('count', 1),
                ('data', returnSerializer.data)
            ])
            # else:
            #     result['code'] = 3003
            #     result['msg'] = f'{fileName}上传超时'
        # objFile = data['file']
        # fileName = objFile.name
        # with open(fileName, 'wb') as f:
        #     for chunk in objFile.chunks():
        #         f.write(chunk)
        # result['msg'] = f'{fileName}上传成功'
            return Response(data)


class UploadFileDetailAPIView(APIView):

    def delete(self, request, pk):
        # self.http_method_names = ['get', 'post', 'delete', 'put']
        result = {'code': 1000, 'msg': None}
        # data = request.data
        file = File.objects.filter(pk=pk).first()
        # serializer = UploadFileSerializer(instance=file, data=data)
        if not file:
            result['code'] = 3003
            result['msg'] = '该文件不存在，无法删除'
            return Response()
        fileName = file.fileName
        if os.path.exists(file.file.path):
            os.remove(file.file.path)
        # os.remove(os.path.join(MEDIA_ROOT, file.file))
        file.delete()
        result['msg'] = f'文件{fileName}删除成功'
        return Response(result)


class QueryFilesAPIView(APIView):

    def get(self, request):
        result = {'code': 1000, 'msg': None}
        # data = request._request.GET
        data = request.query_params
        processId = data['processId']
        file = File.objects.filter(process=processId)
        serializer = UploadFileSerializer(instance=file, many=True)
        data = OrderedDict([
            ('code', 1000),
            ('msg', '访问成功'),
            ('count', len(file)),
            ('data', serializer.data)
        ])
        return Response(data)


class DownloadFileAPIView(APIView):

    def get(self, request):
        result = {'code': 1000, 'msg': None}
        data = request.query_params
        uploadFilePath = data['filePath']

        filePath = os.path.join(settings.BASE_DIR, uploadFilePath)
        fileName = os.path.basename(filePath)
        # file = File.objects.filter(pk=pk).first()
        if not os.path.exists(filePath):
            result['code'] = 3004
            result['msg'] = '该文件不存在，请确定文件之后重新下载'
            return Response(result)
        # filePath = os.path.join(settings.BASE_DIR, file.file.path)
        # with open(filePath, 'rb') as f:
        #     response = HttpResponse(f.read())
        #     response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        #     response['Content-Disposition'] = f'attachment;filename={fileName}'

        response = StreamingHttpResponse(readFile(filePath))
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = f'attachment; filename*=UTF-8"{fileName}"'

        return response


def readFile(filePath, chunkSize=512):
    with open(filePath, 'rb') as f:
        while True:
            chunk = f.read(chunkSize)
            if chunk:
                yield chunk
            else:
                break
# @api_view(['GET'])
# def GetFileInfo(request):
#     result = {'code': 1000, 'msg': None}
#     # data = request._request.GET
#     data = request.query_params
#     processId = data['processId']
#     file = File.objects.filter(process=processId)
#     serializer = UploadFileSerializer(instance=file, many=True)
#     data = OrderedDict([
#         ('code', 1000),
#         ('msg', '访问成功'),
#         ('count', len(file)),
#         ('data', serializer.data)
#     ])
#     return Response(data)
