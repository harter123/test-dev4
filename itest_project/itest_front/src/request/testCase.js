import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const createTestCase = function (data) { //创建项目
    return postRequest('/backend/testCases/', data)
};

export const updateTestCase = function (testCaseId, data) { //编辑项目
    return putRequest(`/backend/testCase/${testCaseId}/`, data)
};

export const deleteTestCase = function (testCaseId) {//删除项目
    return deleteRequest(`/backend/testCase/${testCaseId}/`)
};

export const getTestCase = function (testCaseId) {//删除项目
    return getRequest(`/backend/testCase/${testCaseId}/`)
};

export const getTestCaseList = function (serviceId, size, page) { //获取项目
    return getRequest(`/backend/testCases/?service_id=${serviceId}&page=${page}&size=${size}`)
};