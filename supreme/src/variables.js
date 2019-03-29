// variables.js

export const routerOptions = [
    { path: '/', component: 'Overview' },
    { path: '/users', component: 'Users' },
    { path: '/groups', component: 'Groups' },
    { path: '/hosts', component: 'Hosts' },
    { path: '/about', component: 'About' }
]

export const API_BASE_URL = "http://localhost:8090/api/v1"
export const Endpoints = {
    HOSTS: API_BASE_URL + "/hosts/",
    USERS: API_BASE_URL + "/users/",
    GROUPS: API_BASE_URL + "/groups/",
}