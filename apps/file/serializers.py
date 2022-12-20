from rest_framework.serializers import ModelSerializer
from .models import File

# Create your tests here.


class UploadFileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        fileName = validated_data['fileName']
        file = validated_data['file']
        processId = validated_data['process']
        return File.objects.create(fileName=fileName, file=file, process=processId)
