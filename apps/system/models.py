from django.db import models

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=20)
    icon = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    component = models.CharField(max_length=120)
    parentId = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=120)
    hidden = models.BooleanField(default=False)
    subCount = models.IntegerField()
    menuSort = models.IntegerField()

    def GetChildrenMenuList(self, parentId):
        subMenuList = Menu.objects.filter(parentId=parentId)
        return subMenuList

class Role(models.Model):
    name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    description = models.CharField(max_length=120)
    menu = models.ManyToManyField(to=Menu)



