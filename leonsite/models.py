from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

class File(models.Model):
    name = models.FileField(upload_to='files')
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=10)
    downsum = models.IntegerField(default=0)
    ishide = models.BooleanField(default=False)
    isdelete = models.BooleanField(default=False)