import json

from django.forms import model_to_dict
from django.views.generic import View
from schema import Schema, And, Optional

from interface_app.models.service import Service
from interface_app.utils.response import response_success, response_failed, ErrorCode


class ServiceView(View):
    update_schema = Schema({Optional('name'): And(str, lambda s: 0 < len(s) < 256),
                            Optional('description'): str,
                            Optional('project_id'): int})

    # Optional代表字段是可选   and代表需要满足所有条件

    def get(self, request, service_id, *args, **kwargs):
        """
        请求是单个数据
        :param request:
        :param service_id:
        :param args:
        :param kwargs:
        :return:
        """
        service = Service.objects.filter(id=service_id).first()
        if not service:
            return response_failed(code=ErrorCode.service, message='数据不存在')
        service_dict = model_to_dict(service)
        return response_success(data=service_dict)

    def put(self, request, service_id, *args, **kwargs):
        """
        这个是修改数据
        :param request:
        :param service_id:
        :param args:
        :param kwargs:
        :return:
        """
        service = Service.objects.filter(id=service_id).first()
        if not service:
            return response_failed(code=ErrorCode.service, message='数据不存在')

        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not self.update_schema.is_valid(data):
            return response_failed()

        data = self.update_schema.validate(data)
        if not data:  # 如果没有传数据，就不需要处理
            pass
        else:
            Service.objects.filter(id=service_id).update(**data)
            service = Service.objects.filter(id=service_id).first()

        service_dict = model_to_dict(service)
        return response_success(data=service_dict)

    def delete(self, request, service_id, *args, **kwargs):
        """
        这个是删除数据
        :param request:
        :param service_id:
        :param args:
        :param kwargs:
        :return:
        """
        Service.objects.filter(id=service_id).delete()
        return response_success(data=True)


class ServicesView(View):
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

        services = Service.objects.filter(project_id=project_id)
        ret = []
        for item in services:
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
        service = Service.objects.create(**data)
        service_dict = model_to_dict(service)
        return response_success(data=service_dict)
