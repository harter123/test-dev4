import datetime

from django.core.paginator import Paginator

from interface_app.models.case import TestCase
import json

from django.forms import model_to_dict
from django.views.generic import View
from schema import Schema, And, Optional

from interface_app.utils.response import response_success, response_failed, ErrorCode


def test_case_model_to_dict(case: TestCase):
    if not case:
        return {}
    case_dict = model_to_dict(case)
    if case.create_time:
        case_dict['create_time'] = datetime.datetime.strftime(
            case.create_time, '%Y-%m-%d %H:%M')
    if case.update_time:
        case_dict['update_time'] = datetime.datetime.strftime(
            case.update_time, '%Y-%m-%d %H:%M')
    case_dict['request_body'] = json.loads(case.request_body, encoding="utf-8")
    case_dict['response_assert'] = json.loads(
        case.response_assert, encoding="utf-8")
    return case_dict


class TestCaseView(View):
    update_schema = Schema({
        Optional('service_id'): int,
        Optional('name'): And(str, lambda s: 0 < len(s) < 50),
        Optional('url'): str,
        Optional('method'): int,
        Optional("request_type"): int,
        Optional("request_body"): dict,
        Optional("response"): str,
        Optional("response_assert"): dict
    })

    # Optional代表字段是可选   and代表需要满足所有条件

    def get(self, request, case_id, *args, **kwargs):
        """
        请求是单个数据
        :param request:
        :param case_id:
        :param args:
        :param kwargs:
        :return:
        """
        case = TestCase.objects.filter(id=case_id).first()
        if not case:
            return response_failed(code=ErrorCode.test_case, message='数据不存在')
        ret = test_case_model_to_dict(case)
        return response_success(data=ret)

    def put(self, request, case_id, *args, **kwargs):
        """
        这个是修改数据
        :param request:
        :param case_id:
        :param args:
        :param kwargs:
        :return:
        """
        case = TestCase.objects.filter(id=case_id).first()
        if not case:
            return response_failed(code=ErrorCode.test_case, message='数据不存在')

        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not self.update_schema.is_valid(data):
            return response_failed()

        data = self.update_schema.validate(data)
        if not data:  # 如果没有传数据，就不需要处理
            pass
        else:
            if data.get('request_body'):
                data['request_body'] = json.dumps(data['request_body'], encoding="utf-8")
            if data.get('response_assert'):
                data['response_assert'] = json.dumps(data['response_assert'], encoding="utf-8")
            TestCase.objects.filter(id=case_id).update(**data)
            case = TestCase.objects.filter(id=case_id).first()

        ret = test_case_model_to_dict(case)
        return response_success(data=ret)

    def delete(self, request, case_id, *args, **kwargs):
        """
        这个是删除数据
        :param request:
        :param case_id:
        :param args:
        :param kwargs:
        :return:
        """
        TestCase.objects.filter(id=case_id).delete()
        return response_success(data=True)


class TestCasesView(View):
    create_schema = Schema({
        'service_id': int,
        'name': And(str, lambda s: 0 < len(s) < 50),
        'url': str,
        'method': int,
        "request_type": int,
        Optional("request_body"): dict,
        Optional("response"): str,
        Optional("response_assert"): dict
    })

    def get(self, request, *args, **kwargs):
        """
        请求用例列表数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        service_id = request.GET.get('service_id')
        size = str(request.GET.get('size'))
        page = str(request.GET.get('page'))
        if not size.isdigit() or  not size: #先判断是否是数字,是否为空
            size = 10
        if not page.isdigit() or not page: #先判断是否是数字,是否为空
            page = 1

        size = int(size)
        page = int(page)

        if not service_id:
            return response_success(data=[])

        cases = TestCase.objects.filter(service_id=service_id)
        ret = []

        p = Paginator(cases, size)  # size条数据为一页，实例化分页对象
        page_cases = p.page(page)  # 取第几页
        total = p.count  # 总共元素

        for item in page_cases.object_list:
            tmp = test_case_model_to_dict(item)
            ret.append(tmp)
        return response_success(data={
            "total": total,
            "list": ret
        })

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
        if data.get('request_body'):
            data['request_body'] = json.dumps(data['request_body'], encoding="utf-8")
        if data.get('response_assert'):
            data['response_assert'] = json.dumps(data['response_assert'], encoding="utf-8")

        case = TestCase.objects.create(**data)
        case_dict = test_case_model_to_dict(case)
        return response_success(data=case_dict)
