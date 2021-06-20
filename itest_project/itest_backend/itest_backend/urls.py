"""itest_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from interface_app.views.case_views import TestCaseView, TestCasesView, TestCaseDebugView
from django.contrib import admin
from django.urls import path

import interface_app.user_views as user_views
from interface_app.views.project_views import ProjectsView, ProjectView
from interface_app.views.service_views import ServiceView, ServicesView
from interface_app.views.task_views import TasksView, TaskView, TaskTestCasesView, TaskRunTestCasesView, \
    TaskReportListView, TaskReportDetailView, TaskIntervalRunTestCasesView


def test1(request):
    from django.http.response import HttpResponse
    return  HttpResponse("test1")

def test2(request):
    from django.http.response import HttpResponse
    return  HttpResponse("test2")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/login/', user_views.user_login),
    path('backend/logout/', user_views.user_logout),
    path('backend/user/', user_views.get_user_info),

    path('backend/projects/', ProjectsView.as_view()),
    path('backend/project/<int:project_id>/', ProjectView.as_view()),

    path('backend/services/', ServicesView.as_view()),
    path('backend/service/<int:service_id>/', ServiceView.as_view()),

    path('backend/testCases/', TestCasesView.as_view()),
    path('backend/testCase/<int:case_id>/', TestCaseView.as_view()),
    path('backend/testCase/debug/', TestCaseDebugView.as_view()),

    path('backend/tasks/', TasksView.as_view()),
    path('backend/task/<int:task_id>/', TaskView.as_view()),
    path('backend/task/<int:task_id>/testCases/', TaskTestCasesView.as_view()),

    path('backend/task/<int:task_id>/run/', TaskRunTestCasesView.as_view()),
    path('backend/task/<int:task_id>/interval_run/', TaskIntervalRunTestCasesView.as_view()),

    path('backend/task/<int:task_id>/reports/', TaskReportListView.as_view()),
    path('backend/task/<int:task_id>/report/<str:report_name>/', TaskReportDetailView.as_view()),

    path('test1', test1),
    path('test2', test2),
]
