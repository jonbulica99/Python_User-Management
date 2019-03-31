import Vue from 'vue';
import App from './App.vue';
import router from './router';
import BootstrapVue from 'bootstrap-vue';
import VuejsDialog from 'vuejs-dialog';

// import stylesheets
import 'bootstrap/dist/css/bootstrap.css';
import 'vue-material-design-icons/styles.css';

// use bootstrap
import 'bootstrap';
Vue.use(BootstrapVue)

// dialogs
import 'vuejs-dialog/dist/vuejs-dialog.min.css';
Vue.use(VuejsDialog, {
  html: true,
  loader: false,
  okText: 'Continue',
  cancelText: 'Cancel',
  animation: 'zoom'
})

// progress bar
import BProgress from 'bootstrap-vue/es/components/progress/progress'
Vue.component('b-progress', BProgress)

// material design icons
import MenuIcon from "vue-material-design-icons/Menu.vue"
Vue.component("menu-icon", MenuIcon)
import AccountEditIcon from "vue-material-design-icons/AccountEdit.vue"
Vue.component("edit-icon", AccountEditIcon)
import DeleteOutlineIcon from "vue-material-design-icons/DeleteOutline.vue"
Vue.component("delete-icon", DeleteOutlineIcon)


Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
