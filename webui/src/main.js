import Vue from 'vue'
import App from './App'
import router from './router'
import ChatBox from './components/ChatBox'
import ChatMsg from './components/ChatMsg'

import axios from 'axios'

import './assets/main.css'
// import 'bootstrap/dist/css/bootstrap.css'

Vue.config.productionTip = false
Vue.prototype.$axios = axios

Vue.component('ChatBox', ChatBox)
Vue.component('ChatMsg', ChatMsg)

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
