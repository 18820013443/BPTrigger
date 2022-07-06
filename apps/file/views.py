from django.shortcuts import render
from .serializers import UploadFileSerializer
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from .models import File

# Create your views here.


class UploadFileAPIView(APIView):
    # parser_classes = [FileUploadParser]
    parser_classes = [MultiPartParser]

    def post(self, request):
        result, data = {'code': 1000, 'msg': None}, {}
        dataRequest = request.data
        objFile = dataRequest['file']
        fileName = objFile.name
        data['file'] = objFile
        data['name'] = fileName
        serializer = UploadFileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            if not ('.xls' in fileName or '.csv' in fileName):
                result['code'] = 3001
                result['msg'] = '文件必须为xlsx/xls/csv'
                return Response(result)
            serializer.save()
            result['msg'] = f'{fileName}上传成功'
        # objFile = data['file']
        # fileName = objFile.name
        # with open(fileName, 'wb') as f:
        #     for chunk in objFile.chunks():
        #         f.write(chunk)
        # result['msg'] = f'{fileName}上传成功'
        return Response(result)


class UploadFileDetailAPIView(APIView):

    def delete(self, request, pk):
        result = {'code': 1000, 'msg': None}
        data = request.data
        file = File.objects.filter(pk=pk).first()
        # serializer = UploadFileSerializer(instance=file, data=data)
        if not file:
            result['code'] = 3002
            result['msg'] = '该文件不存在，无法删除'
            return Response(result)
        file.delete()
        result['msg'] = f'文件{file.name}删除成功'
        return Response(result)
        pass

