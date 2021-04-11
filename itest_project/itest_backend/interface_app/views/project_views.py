import json

from django.forms import model_to_dict
from django.views.generic import View
from schema import Schema, And, Optional

from interface_app.models.project import Project
from interface_app.utils.response import response_success, response_failed, ErrorCode


class ProjectView(View):
    update_schema = Schema({Optional('name'): And(str, lambda s: 0 < len(s) < 256),
                            Optional('description'): str})

    # Optional代表字段是可选   and代表需要满足所有条件

    def get(self, request, project_id, *args, **kwargs):
        """
        请求是单个数据
        :param request:
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return response_failed(code=ErrorCode.project, message='数据不存在')
        project_dict = model_to_dict(project)
        return response_success(data=project_dict)

    def put(self, request, project_id, *args, **kwargs):
        """
        这个是修改数据
        :param request:
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return response_failed(code=ErrorCode.project, message='数据不存在')

        body = request.body
        data = json.loads(body, encoding='utf-8')
        if not self.update_schema.is_valid(data):
            return response_failed()

        data = self.update_schema.validate(data)
        if not data:  # 如果没有传数据，就不需要处理
            pass
        else:
            Project.objects.filter(id=project_id).update(**data)
            # 为什么会有三种情况, 因为data的确存在三种情况
            # {"name": 'x'} {"description": 'x'} {"description": 'x', "name": 'x'}
            # Project.objects.filter(id=project_id).update(name='x', description='x')
            # Project.objects.filter(id=project_id).update(name='x')
            # Project.objects.filter(id=project_id).update(description='x')
            project = Project.objects.filter(id=project_id).first()

        project_dict = model_to_dict(project)
        return response_success(data=project_dict)

    def delete(self, request, project_id, *args, **kwargs):
        """
        这个是删除数据
        :param request:
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        Project.objects.filter(id=project_id).delete()
        return response_success(data=True)


class ProjectsView(View):
    create_schema = Schema({'name': And(str, lambda s: 0 < len(s) < 256),
                            'description': str})

    def get(self, request, *args, **kwargs):
        """
        请求列表数据
        :param request:
        :param project_id:
        :param args:
        :param kwargs:
        :return:
        """
        projects = Project.objects.all()
        ret = []
        for item in projects:
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
        project = Project.objects.create(**data)
        project_dict = model_to_dict(project)
        return response_success(data=project_dict)
