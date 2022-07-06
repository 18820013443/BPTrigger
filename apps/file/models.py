from django.db import models

# Create your models here.


class File(models.Model):
    name = models.CharField(max_length=120)
    file = models.FileField(upload_to='InputFiles')
