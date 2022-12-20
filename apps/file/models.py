from django.db import models
from process.models import Process

# Create your models here.


class File(models.Model):
    fileName = models.CharField(max_length=120)
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    file = models.FileField(upload_to='InputFiles')
