import Vue from 'vue'
import Router from 'vue-router'
import User from './views/Users.vue'

const routerOptions = [
  { path: '/', component: 'Users' },
  { path: '/hosts', component: 'Hosts' },
  { path: '/groups', component: 'Groups' },
  { path: '/about', component: 'About' }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/views/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: routes
})
