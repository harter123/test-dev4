# -*- coding: UTF-8 –*-
import requests
import traceback

class HttpRequest:

    @classmethod
    def assert_response(cls, assertions, response):
        """
        # 断言格式:
    # {
    #
    #          "a": "include",
     #         "b": "exclude",
    #
    # }
        :param assertions:
        :param response:
        :return:
        """
        for key in assertions:
            rule =assertions[key]
            if not rule:
                continue

            if rule == "include":
                assert str(key) in str(response)
            elif rule == "exclude":
                assert str(key) not in str(response)
            else:
                continue
        return

    @classmethod
    def send_request(cls, url, method, params, request_type):
        if not url or not method:
            return ""
        ret = ''
        try:
            if "GET" == method or "get" == method or 1 == method:
                ret = cls._get_request(url, params, request_type)
            elif "POST" == method or "post" == method or 2 == method:
                ret = cls._post_request(url, params, request_type)
            elif "DELETE" == method or "delete" == method or 3 == method:
                ret = cls._delete_request(url, params, request_type)
            elif "PUT" == method or "put" == method or 4 == method:
                ret = cls._put_request(url, params, request_type)
            return ret
        except Exception:
            return traceback.format_exc()

    @classmethod
    def _get_request(cls, url, parameter, request_type):
        """
        get请求，数据都在url，超时30s
        :param url: 字符串
        :param parameter: 字典
        :return:
        """
        ret = requests.get(url, params=parameter, timeout=30)
        ret.encoding = 'utf-8'
        return ret.text

    @classmethod
    def common_header(cls, request_type):
        if 1 == request_type:
            header = {
                "content-type": "application/x-www-form-urlencoded"
            }
        else:
            header = {
                "content-type": "application/json"
            }
        return header

    @classmethod
    def _post_request(cls, url, parameter, request_type):
        """
        post 请求
        :param url:
        :param parameter: 字典
        :return:
        """
        header = cls.common_header(request_type)
        ret = requests.post(url, data=parameter, headers=header, timeout=30)
        ret.encoding = 'utf-8'
        return ret.text

    @classmethod
    def _delete_request(cls, url, parameter, request_type):
        """
        delete请求
        :param url:
        :param parameter:
        :return:
        """
        header = cls.common_header(request_type)
        ret = requests.delete(url, data=parameter, headers=header, timeout=30)
        ret.encoding = 'utf-8'
        return ret.text

    @classmethod
    def _put_request(cls, url, parameter, request_type):
        """
        put请求
        :param url:
        :param parameter:
        :return:
        """
        header = cls.common_header(request_type)
        ret = requests.put(url, data=parameter, headers=header, timeout=30)
        ret.encoding = 'utf-8'
        return ret.text