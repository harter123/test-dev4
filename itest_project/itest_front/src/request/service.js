import {deleteRequest, getRequest, postRequest, putRequest} from "./common";

export const createService = function (data) { //创建项目
    return postRequest('/backend/services/', data)
};

export const updateService = function (serviceId, data) { //编辑项目
    return putRequest(`/backend/service/${serviceId}/`, data)
};

export const deleteService = function (serviceId) {//删除项目
    return deleteRequest(`/backend/service/${serviceId}/`)
};

export const getServiceList = function (projectId) { //获取项目
    return getRequest('/backend/services/?project_id=' + projectId)
};