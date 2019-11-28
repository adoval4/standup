import Vue from 'vue'
import App from './App.vue'

// vuex
import store from './store'

// material
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'
Vue.use(VueMaterial)

// vue router
import VueRouter from 'vue-router'
import routes from './routes'
Vue.use(VueRouter)
const router = new VueRouter({ routes, mode: 'history' })

new Vue({
  el: '#app',
  render: h => h(App),
  router: router,
  store: store
})
