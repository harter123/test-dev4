import json

from django.forms import model_to_dict
from django.views.generic import View
from schema import Schema, And, Optional

from interface_app.models.case import TestCase
from interface_app.models.task import Task, TaskTestCase
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