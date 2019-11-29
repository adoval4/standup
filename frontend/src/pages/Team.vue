<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <md-button class="md-icon-button" :to="{ name: 'home' }">
          <md-icon>arrow_back</md-icon>
        </md-button>
        <span v-if="team" class="md-title logo">
          Standup - {{ team.name }}
        </span>
      </md-app-toolbar>

      <md-app-content >
        <md-progress-bar
          md-mode="indeterminate"
          v-if="!team"
        >
        </md-progress-bar>


      </md-app-content>
    </md-app>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      team: {
        id: 'asdasdqe12e12e21asdsad',
        name: 'Daily',
        members: [
          {
            id: 'asdadsadsadsad',
            name: 'Pedro',
            goals: [
              {
                id: 'asdadekd9293123',
                description: 'Get task 1 done',
                status: null
              }
            ]
          },
          {
            id: 'asdadsadsasdaddsad',
            name: 'Pedro 2',
            goals: [
              {
                id: 'asdadekd9293123',
                description: 'Get task 1 done',
                status: null
              }
            ]
          },
        ]
      }
    }
  },
  // computed: {
  //   team() {
  //     return this.$store.state.team;
  //   }
  // },
  created() {
    this.$store.dispatch('getTeam', {
      teamId: this.$route.params.teamId
    });
  }
}
</script>

<style lang="css" scoped>
</style>
