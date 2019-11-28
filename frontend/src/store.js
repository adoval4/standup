import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex)


const store = new Vuex.Store({
  state: {
    user: null
  },
  mutations: {
    retrieveUserFromLocalStorage (state) {
      if(!localStorage.authenticatedUser) { return; }
      state.user = JSON.parse(localStorage.authenticatedUser);
    },
    setUser (state, payload = {}) {
      if(!payload.user) { return; }
      localStorage.authenticatedUser = JSON.stringify(payload.user);
      state.user = payload.user;
    },
    logoutUser (state) {
      localStorage.removeItem('authenticatedUser');
      state.user = null;
    }
  }
});

export default store;