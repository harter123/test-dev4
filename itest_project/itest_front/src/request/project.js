import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const createProject = function (data) { //创建项目
    return postRequest('/backend/projects/', data)
};

export const updateProject = function (projectId, data) { //编辑项目
    return putRequest(`/backend/project/${projectId}/`, data)
};

export const deleteProject = function (projectId) {//删除项目
    return deleteRequest(`/backend/project/${projectId}/`)
};

export const getProjectList = function () { //获取项目
    return getRequest('/backend/projects/')
};