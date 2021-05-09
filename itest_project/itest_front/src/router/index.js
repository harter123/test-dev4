import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/main.vue'
import project from '../views/project.vue'
import login from '../views/login.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'project',
        component: project
    },
    {
        path: '/main',
        name: 'main',
        component: Main,
        children: [
            {
                path: 'service',
                name: 'service',
                component: () => import('../views/service/index.vue'),
            },
            {
                path: 'interface',
                name: 'interface',
                component: () => import('../views/interface/index.vue'),
            },
            {
                path: 'task',
                name: 'task',
                component: () => import('../views/task/index.vue'),
            },
        ]
    },
    {
        path: '/login',
        name: 'login',
        component: login
    },
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
