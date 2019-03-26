import Vue from 'vue'
import App from './App.vue'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
import VuejsDialog from "vuejs-dialog"

import 'bootstrap/dist/css/bootstrap.css'
import 'vue-material-design-icons/styles.css'

// use bootstrap
Vue.use(BootstrapVue)

// dialogs
import 'vuejs-dialog/dist/vuejs-dialog.min.css';
Vue.use(VuejsDialog)

// material design icons
import MenuIcon from "vue-material-design-icons/Menu.vue"
import AccountEditIcon from "vue-material-design-icons/AccountEdit.vue"
import DeleteOutlineIcon from "vue-material-design-icons/DeleteOutline.vue"

Vue.component("menu-icon", MenuIcon)
Vue.component("edit-icon", AccountEditIcon)
Vue.component("delete-icon", DeleteOutlineIcon)

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
