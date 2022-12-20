from django.db import models
from system.models import Role

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.ManyToManyField(to=Role)



