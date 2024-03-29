# Generated by Django 3.1.2 on 2021-05-16 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface_app', '0003_auto_20210418_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.IntegerField(db_index=True, verbose_name='服务id')),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('url', models.TextField(verbose_name='URL')),
                ('method', models.IntegerField(default=1, verbose_name='请求方法')),
                ('request_type', models.IntegerField(default=1, verbose_name='参数类型')),
                ('request_body', models.TextField(verbose_name='参数内容')),
                ('response', models.TextField(verbose_name='结果')),
                ('response_assert', models.TextField(verbose_name='断言')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]
