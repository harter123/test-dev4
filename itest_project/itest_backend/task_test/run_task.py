# -*- coding: UTF-8 –*-
import pytest
import os
import sys
import django
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 定位到你的django根目录
sys.path.append(os.path.abspath(os.path.join(BASE_DIR, os.pardir)))  # 把django目录放到环境变量里面
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itest_backend.settings")  # django项目的配置，你的django的settings文件
django.setup()  # django的初始化

from interface_app.models.task import TaskTestCase, RunTask
from interface_app.models.case import TestCase
from task_test.http_request import HttpRequest
#
run_task = RunTask.objects.all().first()  # 1. 提供一个任务id
if run_task is None:
    exit(-1)
task_id = run_task.task_id

# RunTask.objects.filter(id=run_task.id).delete()

params_list = []  # 这是参数列表

 # 2.获取任务所有的接口
task_i_s = TaskTestCase.objects.filter(task_id=task_id)
for item in task_i_s:
    case = TestCase.objects.filter(id=item.test_case_id).first()
    item_data = [
        case.name,
        case.method,
        case.url,
        json.loads(case.request_body, encoding="utf-8"),
        json.loads(case.response_assert, encoding="utf-8"),
        case.request_type
    ]
    params_list.append(item_data)  # 3. 这是构造参数化列表

@pytest.mark.parametrize(("name", "method", "url", "params", "assertions", "request_type"), params_list)
def test_task(name, method, url, params, assertions, request_type):
    response = HttpRequest.send_request(url, method, params, request_type)  # 4. 进行http请求，获取响应
    HttpRequest.assert_response(assertions,response) # 5. 断言格式
