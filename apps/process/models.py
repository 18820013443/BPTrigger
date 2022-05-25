from django.db import models
from account.models import Account

# Create your models here.


class Process(models.Model):
    processName = models.CharField(max_length=1000)
    postBody = models.TextField(max_length=100000)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
