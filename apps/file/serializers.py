from rest_framework.serializers import ModelSerializer
from .models import File

# Create your tests here.


class UploadFileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data['name']
        file = validated_data['file']
        return File.objects.create(name=name, file=file)
