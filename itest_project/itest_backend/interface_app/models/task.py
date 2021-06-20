from django.db import models

# Create your models here.

class Task(models.Model):
    project_id = models.IntegerField('project_id', db_index=True)
    name = models.CharField("name",max_length=255, null=False)
    description = models.TextField('描述')

    days = models.IntegerField('days', null=True, default=0)
    hours = models.IntegerField('hour', null=True, default=0)
    minutes = models.IntegerField('minutes', null=True, default=0)
    start_time = models.DateTimeField('start_time', null=True, default=None) #循环的开始时间
    interval_switch = models.BooleanField('interval_switch', default=False) # 代表是否开启了循环执行


class TaskTestCase(models.Model):
    # 任务和案例的关联表
    task_id = models.IntegerField('task id', db_index=True)
    test_case_id = models.IntegerField('case id', db_index=True)


class RunTask(models.Model):
    task_id = models.IntegerField('任务id', default=0)
