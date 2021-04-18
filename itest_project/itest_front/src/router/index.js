import Vue from 'vue'
import VueRouter from 'vue-router'
// import Home from '../views/Home.vue'
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
