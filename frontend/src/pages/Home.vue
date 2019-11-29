<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo">Standup</span>
      </md-app-toolbar>

      <md-app-content >
        <md-progress-bar
          md-mode="indeterminate"
          v-if="!teams"
        >
        </md-progress-bar>

        <md-list v-if="teams && teams.length > 0">

          <md-subheader>My teams</md-subheader>

          <md-list-item
            v-for="team in teams"
            :key="team.id"
            :to="`/${team.id}`"
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
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newTeamName: null,
    }
  },
  created() {
    // get teams
    this.$store.dispatch('getTeams');
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
    },
    createNewGroup: function() {
      this.$store.dispatch('createTeam', {
        name: this.newTeamName
      });
      this.newTeamName = null;
    }
  }
}
</script>

<style lang="css" scoped>
</style>
