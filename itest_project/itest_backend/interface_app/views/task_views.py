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
        print(command)
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
        if not os.path.exists(task_reports_path):
            return response_success(list_name)

        for file in os.listdir(task_reports_path):
            if os.path.splitext(file)[1] == '.html':
                list_name.append({"name": file})
        return response_success(list_name)


class TaskReportDetailView(View):
    def get(self, request, task_id, report_name, *args, **kwargs):
        """
        获取report列表
        :param request:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task_report_path = os.path.join(settings.BASE_DIR, "task_test", "reports", str(task_id), report_name)

        if not os.path.exists(task_report_path):
            return HttpResponse()
        else:
            # 把 assets/style.css 替换为 为style,不替代会有样式问题
            file = open(task_report_path, "rt", encoding='utf-8')
            html_context = file.read()
            html_context = str(html_context)

            style = """
            <style>
      body {
	font-family: Helvetica, Arial, sans-serif;
	font-size: 12px;
	/* do not increase min-width as some may use split screens */
	min-width: 800px;
	color: #999;
}

h1 {
	font-size: 24px;
	color: black;
}

h2 {
	font-size: 16px;
	color: black;
}

p {
    color: black;
}

a {
	color: #999;
}

table {
	border-collapse: collapse;
}

/******************************
 * SUMMARY INFORMATION
 ******************************/

#environment td {
	padding: 5px;
	border: 1px solid #E6E6E6;
}

#environment tr:nth-child(odd) {
	background-color: #f6f6f6;
}

/******************************
 * TEST RESULT COLORS
 ******************************/
span.passed, .passed .col-result {
	color: green;
}
span.skipped, span.xfailed, span.rerun, .skipped .col-result, .xfailed .col-result, .rerun .col-result {
	color: orange;
}
span.error, span.failed, span.xpassed, .error .col-result, .failed .col-result, .xpassed .col-result  {
	color: red;
}


/******************************
 * RESULTS TABLE
 *
 * 1. Table Layout
 * 2. Extra
 * 3. Sorting items
 *
 ******************************/

/*------------------
 * 1. Table Layout
 *------------------*/

#results-table {
	border: 1px solid #e6e6e6;
	color: #999;
	font-size: 12px;
	width: 100%
}

#results-table th, #results-table td {
	padding: 5px;
	border: 1px solid #E6E6E6;
	text-align: left
}
#results-table th {
	font-weight: bold
}

/*------------------
 * 2. Extra
 *------------------*/

.log:only-child {
	height: inherit
}
.log {
	background-color: #e6e6e6;
	border: 1px solid #e6e6e6;
	color: black;
	display: block;
	font-family: "Courier New", Courier, monospace;
	height: 230px;
	overflow-y: scroll;
	padding: 5px;
	white-space: pre-wrap
}
div.image {
	border: 1px solid #e6e6e6;
	float: right;
	height: 240px;
	margin-left: 5px;
	overflow: hidden;
	width: 320px
}
div.image img {
	width: 320px
}
div.video {
	border: 1px solid #e6e6e6;
	float: right;
	height: 240px;
	margin-left: 5px;
	overflow: hidden;
	width: 320px
}
div.video video {
	overflow: hidden;
	width: 320px;
    height: 240px;
}
.collapsed {
	display: none;
}
.expander::after {
	content: " (show details)";
	color: #BBB;
	font-style: italic;
	cursor: pointer;
}
.collapser::after {
	content: " (hide details)";
	color: #BBB;
	font-style: italic;
	cursor: pointer;
}

/*------------------
 * 3. Sorting items
 *------------------*/
.sortable {
	cursor: pointer;
}

.sort-icon {
	font-size: 0px;
	float: left;
	margin-right: 5px;
	margin-top: 5px;
	/*triangle*/
	width: 0;
	height: 0;
	border-left: 8px solid transparent;
	border-right: 8px solid transparent;
}

.inactive .sort-icon {
	/*finish triangle*/
	border-top: 8px solid #E6E6E6;
}

.asc.active .sort-icon {
	/*finish triangle*/
	border-bottom: 8px solid #999;
}

.desc.active .sort-icon {
	/*finish triangle*/
	border-top: 8px solid #999;
}

  </style>
            """

            html_context = html_context.replace('<link href="assets/style.css" rel="stylesheet" type="text/css"/></head>', style)

            new_file = open(task_report_path, "w", encoding='utf-8')
            new_file.write(html_context)

            return render(request, str(task_id) + "/" + report_name)