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

      <md-app-content class="md-scrollbar" >
        <md-progress-bar
          id="top-progress-bar"
          md-mode="indeterminate"
          v-if="loading"
        >
        </md-progress-bar>

        <md-card >

          <md-card-header class="md-layout-item">
            <div class="md-title">Pending invitations</div>
            <div class="md-subhead"></div>
          </md-card-header>

          <md-card-content >
            <md-list >
              <invitation
                :invitation="">
              </invitation >

            </md-list>

          </md-card-content>
        </md-card>

        <md-card v-if="pendingGoalsByTeam">

          <md-card-header class="md-layout-item">
            <div class="md-title">My goals</div>
            <div class="md-subhead"></div>
          </md-card-header>

          <md-card-content >
            <md-list >
              <div
                v-for="_team in pendingGoalsByTeam"
                :key="_team.id"
                :md-ripple="false"
              >
                <md-subheader>
                  <router-link :to="`/${_team.id}`">{{ _team.name }}</router-link>
                </md-subheader>

                <goal-item
                  v-for="_goal in _team.goals"
                  :goalId="_goal.id"
                  :memberId="_team.membership"
                  :key="_goal.id"
                >
                </goal-item>

                <md-list-item v-if="_team.goals.length == 0" class="text-muted">
                  No pending goals for now
                </md-list-item>

              </div>
            </md-list>
          </md-card-content>

        </md-card>

        <md-card>
          <md-card-header class="md-layout-item">
            <div class="md-title"> My teams </div>
            <div class="md-subhead">Where I'm a manager</div>
          </md-card-header>

          <md-card-content >
            <md-list v-if="teams && teams.length > 0">
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

          </md-card-content>

        </md-card>

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
import GoalItem from '../components/GoalItem.vue'
import Invitation from '../components/Invitation.vue'
import ServerUnreachableSnackbar from '../components/ServerUnreachableSnackbar.vue';

export default {
  components: {
    'goal-item': GoalItem,
    'invitation': Invitation,
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
    const res_goals = this.$store.dispatch('getMyPendingGoalsByTeam');
    res_goals.finally(() => { this.loading = false })
    const res_teams = this.$store.dispatch('getTeams');
    res_teams.finally(() => { this.loading = false })
  },
  computed: {
    user: function() {
      return this.$store.state.user;
    },
    teams: function() {
      return this.$store.state.teams;
    },
    pendingGoalsByTeam: function() {
      return this.$store.state.pendingGoalsByTeam;
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

<style lang="scss" scoped>

#top-progress-bar {
  position: absolute;
  width: 100%;
  left: 0px;
  margin-top: -16px;
}

.md-card {
  margin-top: 1.5em;
  margin-bottom: 2.5em;
}

</style>
