from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    # 1代表正常  2代表关闭
    status = models.IntegerField(null=False, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
