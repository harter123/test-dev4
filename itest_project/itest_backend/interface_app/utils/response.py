from django.http import JsonResponse


class ErrorCode:
    common = 10000
    auth = 10001
    project = 10002
    service = 10003
    test_case = 10004


# 这是一个通用的
def common_response(success, data, error_code, error_message):
    response = {
        "data": data,
        "success": success, #布尔型，成功或者是失败的标志
        "error": {
            "code": error_code,  # 错误码
            "message": error_message
        }
    }
    return JsonResponse(response, safe=False)


# 这两个是快捷方式
def response_success(data=None):
    if data is None:
        data = {}
    return common_response(True, data, "", "")


def response_failed(code=ErrorCode.common, message="参数错误", data=None):
    if data is None:
        data = {}
    return common_response(False, data, code, message)
