from django.db import models

# Create your models here.


class Process(models.Model):
    processName = models.CharField(max_length=1000)
    postBody = models.TextField(max_length=100000)
    email = models.CharField(max_length=100)
