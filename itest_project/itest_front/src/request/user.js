import {deleteRequest, getRequest, postRequest} from "./common";

export const login = function (username, password) { //登录
    return postRequest('/backend/login/', {
        name: username,
        psw: password,
    })
};

export const logout = function () {//退出登录
    return deleteRequest('/backend/logout/')
};

export const getLoginUserInfo = function () { //获取已经登录的用户信息
    return getRequest('/backend/user/')
};