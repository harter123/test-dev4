import datetime
import json
import os

from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from schema import Schema, And, Optional

from interface_app.models.case import TestCase
from interface_app.models.task import Task, TaskTestCase, RunTask
from interface_app.utils.response import response_success, response_failed, ErrorCode
from interface_app.views.case_views import test_case_model_to_dict


class TaskView(View):
    update_schema = Schema({Optional('name'): And(str, lambda s: 0 < len(s) < 256),
                            Optional('description'): str,
                            Optional('project_id'): int})

    # Optional代表字段是可选   and代表需要满足所有条件

    def get(self, request, task_id, *args, **kwargs):
        """
        请求是单个数据
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return response_failed(code=ErrorCode.task, message='数据不存在')
        task_dict = model_to_dict(task)
        return response_success(data=task_dict)

    def put(self, request, task_id, *args, **kwargs):
        """
        这个是修改数据
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return response_failed(code=ErrorCode.task, message='数据不存在')

        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not self.update_schema.is_valid(data):
            return response_failed()

        data = self.update_schema.validate(data)
        if not data:  # 如果没有传数据，就不需要处理
            pass
        else:
            Task.objects.filter(id=task_id).update(**data)
            task = Task.objects.filter(id=task_id).first()

        task_dict = model_to_dict(task)
        return response_success(data=task_dict)

    def delete(self, request, task_id, *args, **kwargs):
        """
        这个是删除数据
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        Task.objects.filter(id=task_id).delete()
        return response_success(data=True)


class TasksView(View):
    create_schema = Schema({'name': And(str, lambda s: 0 < len(s) < 256),
                            'description': str,
                            'project_id': int})

    def get(self, request, *args, **kwargs):
        """
        请求列表数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        project_id = request.GET.get('project_id')
        if not project_id:
            return response_success(data=[])

        tasks = Task.objects.filter(project_id=project_id)
        ret = []
        for item in tasks:
            ret.append(model_to_dict(item))
        return response_success(data=ret)

    def post(self, request, *args, **kwargs):
        """
        创建数据
        :param request:
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not self.create_schema.is_valid(data):
            return response_failed()

        data = self.create_schema.validate(data)
        task = Task.objects.create(**data)
        task_dict = model_to_dict(task)
        return response_success(data=task_dict)


class TaskTestCasesView(View):
    def get(self, request, task_id, *args, **kwargs):
        """
        请求任务的用例列表数据
        :param request:
        :param args:
        :param task_id:
        :param kwargs:
        :return:
        """
        task_cases = TaskTestCase.objects.filter(task_id=task_id)
        ret = []
        for item in task_cases:
            case = TestCase.objects.get(id=item.test_case_id)
            tmp = test_case_model_to_dict(case)
            tmp['task_test_case_id'] = item.id
            ret.append(tmp)
        return response_success(data=ret)

    def post(self, request, task_id, *args, **kwargs):
        """
        创建数据
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        create_schema = Schema({'test_case_ids': list})

        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not create_schema.is_valid(data):
            return response_failed()
        data = create_schema.validate(data)

        test_case_ids = data['test_case_ids']
        for item in test_case_ids:
            TaskTestCase.objects.create(task_id=task_id, test_case_id=item)
        return response_success()

    def delete(self, request, task_id, *args, **kwargs):
        """
        删除数据
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task_test_case_id = request.GET.get('task_test_case_id')
        if not task_test_case_id:
            return response_success()

        TaskTestCase.objects.filter(id=task_test_case_id).delete()
        return response_success()


class TaskRunTestCasesView(View):
    def post(self, request, task_id, *args, **kwargs):
        """
        任务执行
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task_reports_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id))
        if not os.path.exists(task_reports_path):
            os.makedirs(task_reports_path)

        RunTask.objects.create(task_id=task_id)

        # 组装命令 pytest  run_task.py --html=xxx.html
        now = datetime.datetime.now()
        report_name = now.strftime("%Y-%m-%d-%H-%M-%S") + ".html"

        run_task_path = os.path.join(settings.BASE_DIR, "task_test", "run_task.py")
        report_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id), report_name)
        command = "pytest " + run_task_path + " --html=" + report_path
        os.system(command)

        return response_success()


class TaskReportListView(View):
    def get(self, request, task_id, *args, **kwargs):
        """
        获取report列表
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task_reports_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id))
        list_name = []
        for file in os.listdir(task_reports_path):
            if os.path.splitext(file)[1] == '.html':
                list_name.append(file)
        return response_success(list_name)


class TaskReportDetailView(View):
    def get(self, request, task_id, *args, **kwargs):
        """
        获取report列表
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        report_name = request.GET.get('report_name')
        task_report_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id), report_name)

        if not os.path.exists(task_report_path):
            return HttpResponse()
        else:
            # 把 assets/style.css 替换为 /static/assets/style.css
            # file = open(task_report_path, "rt", encoding='utf-8')
            # html_context = file.read()
            # html_context = str(html_context)
            # html_context = html_context.replace('href="assets/style.css"', 'href="/api_static/assets/style.css"')
            #
            # new_file = open(task_report_path, "w", encoding='utf-8')
            # new_file.write(html_context)


            return render(request, str(task_id) + "/" + report_name)