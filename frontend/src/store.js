import Vue from 'vue'
import Vuex from 'vuex'


import ApiClient from './services/api_client'


Vue.use(Vuex)


const store = new Vuex.Store({
  state: {
    user: null,
    teams: null,
    team: null
  },
  mutations: {
    getUserFromLocalStorage (state) {
      if(!localStorage.authenticatedUser) { return; }
      state.user = JSON.parse(localStorage.authenticatedUser);
    },
    setUser (state, payload = {}) {
      if(!payload.user) { return; }
      localStorage.authenticatedUser = JSON.stringify(payload.user);
      state.user = payload.user;
    },
    setTeams (state, payload = {}) {
      if(!payload.teams) { return; }
      state.teams = payload.teams;
    },
    setTeam (state, payload = {}) {
      if(!payload.team) { return; }
      state.team = payload.team;
    },
    addTeam (state, payload = {}) {
      if(!payload.team) { return; }
      state.teams.push(payload.team);
    },
    logoutUser (state) {
      localStorage.removeItem('authenticatedUser');
      state.user = null;
    }
  },
  actions: {
    getTeams(context) {
      if(!context.state.user) { return; }

      const res = ApiClient.getTeams(context.state.user.token);

      res.then((response) => {
        context.commit('setTeams', {
          teams: response.data.results
        })
      }).catch((error) => {
        console.log(error);
      });
    },
    getTeam(context, payload = {}) {
      if(!context.state.user) { return; }

      const res = ApiClient.retrieveTeam(
        context.state.user.token,
        payload.teamId
      );

      res.then((response) => {
        context.commit('setTeam', {
          team: response.data
        })
      }).catch((error) => {
        console.log(error);
      });
    },
    createTeam(context, payload = {}) {
      if(!context.state.user) { return; }
      if(!payload.name) { return; }

      const res = ApiClient.createTeam(
        context.state.user.token,
        payload.name
      );

      res.then((response) => {
        context.commit('addTeam', {
          team: response.data
        })
      }).catch((error) => {
        console.log(error);
      });
    }
  }
});

export default store;