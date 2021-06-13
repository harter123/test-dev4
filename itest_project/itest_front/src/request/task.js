import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const createTask = function (data) { //创建任务
    return postRequest('/backend/tasks/', data)
};

export const updateTask = function (taskId, data) { //编辑任务
    return putRequest(`/backend/task/${taskId}/`, data)
};

export const deleteTask = function (taskId) {//删除任务
    return deleteRequest(`/backend/task/${taskId}/`)
};

export const getTaskList = function (projectId) { //获取任务
    return getRequest('/backend/tasks/?project_id=' + projectId)
};


export const addTaskTestCase = function (taskId, data) { //任务添加用例
    return postRequest(`/backend/task/${taskId}/testCases/`, data)
};

export const deleteTaskTestCase = function (taskId, taskTestCaseId) {//任务删除用例
    return deleteRequest(`/backend/task/${taskId}/testCases/?task_test_case_id=${taskTestCaseId}`)
};

export const getTaskTestCaseList = function (taskId) { //获取任务的所有用例
    return getRequest(`/backend/task/${taskId}/testCases/`)
};

export const runTask = function (taskId) { //执行任务
    return postRequest(`/backend/task/${taskId}/run/`)
};

export const getTaskReports = function (taskId) { //执行任务
    return getRequest(`/backend/task/${taskId}/reports/`)
};