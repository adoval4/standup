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
    getUserFromLocalStorage(state) {
      if(!localStorage.authenticatedUser) { return; }
      state.user = JSON.parse(localStorage.authenticatedUser);
    },
    setUser(state, payload = {}) {
      if(!payload.user) { return; }
      localStorage.authenticatedUser = JSON.stringify(payload.user);
      state.user = payload.user;
    },
    setTeams(state, payload = {}) {
      if(!payload.teams) { return; }
      state.teams = payload.teams;
    },
    setTeam(state, payload = {}) {
      if(!payload.team) { return; }
      state.team = payload.team;
    },
    addTeam(state, payload = {}) {
      if(!payload.team) { return; }
      state.teams.push(payload.team);
    },
    addTeamMember(state, payload = {}) {
      if(!payload.member) { return; }
      state.team.members.push(payload.member);
    },
    addMemberGoal(state, payload = {}) {
      if(!payload.memberId) { return; }
      if(!payload.goal) { return; }

      for(let i=0; state.team.members.length; i++) {
        if(state.team.members[i].id == payload.memberId) {
          state.team.members[i].goals.push(payload.goal);
          break;
        }
      }
    },
    updateStatusGoal(state, payload = {}) {
      if(!payload.memberId) { return; }
      if(!payload.goalId) { return; }
      if(!payload.status) { return; }

      for(let i=0; state.team.members.length; i++) {
        if(state.team.members[i].id == payload.memberId) {
          for(let j=0; state.team.members[i].goals.length; j++) {
            if(state.team.members[i].goals[j].id == payload.goalId) {
              state.team.members[i].goals[j].status = payload.status;
              break;
            }
          }
          break;
        }
      }
    },
    logoutUser(state) {
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
    },
    createTeamMember(context, payload = {}) {
      if(!context.state.user) { return; }
      if(!context.state.team) { return; }
      if(!payload.name) { return; }
      if(!payload.email) { return; }

      const res = ApiClient.createTeamMember(
        context.state.user.token,
        context.state.team.id,
        payload.name,
        payload.email
      );

      res.then((response) => {
        context.commit('addTeamMember', {
          member: response.data
        })
      }).catch((error) => {
        console.log(error);
      });
    },
    createNewMemberGoal(context, payload = {}) {
      if(!context.state.user) { return; }
      if(!context.state.team) { return; }
      if(!payload.memberId) { return; }
      if(!payload.description) { return; }

      const res = ApiClient.createMemberGoal(
        context.state.user.token,
        payload.memberId,
        payload.description
      );

      res.then((response) => {
        context.commit('addMemberGoal', {
          memberId: payload.memberId,
          goal: response.data
        })
      }).catch((error) => {
        console.log(error);
      });
    },
    updateGoalStatus(context, payload = {}) {

      console.log(payload);

      if(!context.state.user) { return; }
      if(!context.state.team) { return; }
      if(!payload.memberId) { return; }
      if(!payload.goalId) { return; }
      if(!payload.status) { return; }


      const res = ApiClient.updateGoalStatus(
        context.state.user.token,
        payload.goalId,
        payload.status
      );

      res.then((response) => {
        context.commit('updateStatusGoal', {
          memberId: payload.memberId,
          goalId: payload.goalId,
          status: status
        })
      }).catch((error) => {
        console.log(error);
      });
    }
  }
});

export default store;