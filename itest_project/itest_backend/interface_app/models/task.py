from django.db import models

# Create your models here.

class Task(models.Model):
    project_id = models.IntegerField('project_id', db_index=True)
    name = models.CharField("name",max_length=255, null=False)
    description = models.TextField('描述')


class TaskTestCase(models.Model):
    # 任务和案例的关联表
    task_id = models.IntegerField('task id', db_index=True)
    test_case_id = models.IntegerField('case id', db_index=True)