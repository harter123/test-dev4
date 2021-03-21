import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from schema import Schema

from interface_app.utils.response import response_failed, ErrorCode, response_success

user_schema = Schema({"name": str, "psw": str})

@require_http_methods(['POST'])
def user_login(request, *args, **kwargs):
    """
    登录
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    body = request.body
    data = json.loads(body, encoding='utf-8')

    if not user_schema.is_valid(data):
        return response_failed()

    if User.objects.filter(username=data["name"]).exists():
        user = authenticate(username=data["name"], password=data["psw"])
    else:
        user = User.objects.create_user(username=data["name"], password=data["psw"])
    if not user:
        return response_failed(code=ErrorCode.auth, message='登录失败')
    else:
        login(request, user)  # 登录持久化
        return response_success()

@require_http_methods(['DELETE'])
def user_logout(request, *args, **kwargs):
    """
    注销
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    logout(request)
    return response_success()

@require_http_methods(['GET'])
def get_user_info(request, *args, **kwargs):
    """
    获取已登录的用户信息
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    user = request.user # 获取当前用户
    if not user:
        return response_failed(code=ErrorCode.auth, message='用户未登录')
    if user.is_authenticated:  # 判断用户是否已经通过校验
        return response_success(data={
            'id': user.id,
            'name': user.username
        })
    else:
        return response_failed(code=ErrorCode.auth, message='用户未登录')


