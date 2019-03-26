import Vue from 'vue'
import Router from 'vue-router'
import User from './views/Users.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'users',
      component: User
    },
    {
      path: '/hosts',
      name: 'hosts',
      component: () => import('./views/Hosts.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('./views/About.vue')
    }
  ]
})
