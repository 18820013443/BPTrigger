import email
from django.db import models


# Create your models here.
class Account(models.Model):
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)


