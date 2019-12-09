<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo" style="flex: 1">Standup</span>

        <md-menu md-size="medium" md-align-trigger>
          <md-avatar class="md-avatar-icon md-primary" md-menu-trigger>
            <md-icon>account_circle</md-icon>
          </md-avatar>

          <md-menu-content>
            <md-menu-item @click="logoutUser" >
              Logout
            </md-menu-item>
          </md-menu-content>
        </md-menu>

      </md-app-toolbar>

      <md-app-content >
        <md-progress-bar
          id="top-progress-bar"
          md-mode="indeterminate"
          v-if="loading"
        >
        </md-progress-bar>

        <md-list v-if="teams && teams.length > 0">

          <md-subheader>My teams</md-subheader>

          <md-list-item
            v-for="team in teams"
            :key="team.id"
            :to="`/${team.id}`"
            :md-ripple="false"
          >
            <span
              class="md-list-item-text"
            >
              {{ team.name }}
            </span>

          </md-list-item>

          <md-list-item>
            <md-field>
              <label>+ Create a new team</label>
              <md-input
                v-model="newTeamName"
                @keyup.enter="createNewGroup"
              ></md-input>
            </md-field>
          </md-list-item>
        </md-list>

        <md-empty-state
          v-if="teams && teams.length == 0"
          md-label="Create your first team"
          md-description="Creating a team, you'll be able to add yout team members and their goals.">
          <md-field>
            <label>Team name</label>
            <md-input
              v-model="newTeamName"
              @keyup.enter="createNewGroup"
            ></md-input>
          </md-field>
        </md-empty-state>

        <server-unreachable-snackbar></server-unreachable-snackbar>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import ServerUnreachableSnackbar from '../components/ServerUnreachableSnackbar.vue';

export default {
  components: {
    'server-unreachable-snackbar': ServerUnreachableSnackbar
  },
  data() {
    return {
      newTeamName: null,
      loading: true,
    }
  },
  created() {
    // get teams
    const res = this.$store.dispatch('getTeams');
    res.finally(() => { this.loading = false })
  },
  computed: {
    user: function() {
      return this.$store.state.user;
    },
    teams: function() {
      return this.$store.state.teams;
    }
  },
  methods: {
    logoutUser: function() {
      this.$store.commit('logoutUser');
      this.$router.push('/login');
    },
    createNewGroup: function() {
      this.$store.dispatch('createTeam', {
        name: this.newTeamName
      });
      this.newTeamName = null;
    },
  }
}
</script>

<style lang="css" scoped>

#top-progress-bar {
  position: absolute;
  width: 100%;
  left: 0px;
  margin-top: -16px;
}

</style>
