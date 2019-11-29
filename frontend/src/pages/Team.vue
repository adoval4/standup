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

        <md-card
          v-for="member in team.members"
          class="member-card"
        >
          <md-card-header>
            <div class="md-title">{{ member.name }}</div>
            <div class="md-subhead">{{ member.email }}</div>
          </md-card-header>

          <md-card-content>
            <md-list>
              <md-list-item
                v-for="goal in member.goals"
              >
                <span>
                  <span class="progress-radio-btn">
                    <md-radio
                      v-model="goal.status"
                      value="NOT_DONE"
                      class="radio-not-done"
                    ></md-radio>
                    <md-tooltip md-direction="top">Not done</md-tooltip>
                  </span>

                  <span class="progress-radio-btn">
                    <md-radio
                      v-model="goal.status"
                      value="IN_PROGRESS"
                      class="radio-in-progress"
                    ></md-radio>
                    <md-tooltip md-direction="top">In progress</md-tooltip>
                  </span>

                  <span class="progress-radio-btn">
                    <md-radio
                      v-model="goal.status"
                      value="DONE"
                      class="radio-done"
                    ></md-radio>
                    <md-tooltip md-direction="top">Done</md-tooltip>
                  </span>

                </span>
                <span class="md-list-item-text">{{ goal.description }}</span>
                <span class="text-muted">Since 2 days</span>
                <md-button class="md-icon-button">
                  <md-icon>close</md-icon>
                </md-button>
              </md-list-item>

              <md-list-item class="new-goal-list-item">
                <span>
                  <span class="progress-radio-btn">
                    <md-radio disabled></md-radio>
                  </span>

                  <span class="progress-radio-btn">
                    <md-radio disabled></md-radio>
                  </span>

                  <span class="progress-radio-btn">
                    <md-radio disabled></md-radio>
                  </span>

                </span>
                <span class="md-list-item-text">
                  <md-field
                    class="new-goal-input"
                    md-inline
                  >
                    <label>+ New goal for {{ member.name }}</label>
                    <md-input v-model="member.newGoalDescription"></md-input>
                  </md-field>
                </span>
              </md-list-item>

            </md-list>
          </md-card-content>
        </md-card>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      status: null,
      team: {
        id: 'asdasdqe12e12e21asdsad',
        name: 'Daily',
        members: [
          {
            id: 'asdadsadsadsad',
            name: 'Pedro',
            email: 'p@sapasd.com',
            goals: [
              {
                id: 'asdadekd9293123',
                description: 'Get task 1 done',
                status: null
              },
              {
                id: 'asdadekd9293123',
                description: 'Get task 1 done',
                status: 'DONE'
              },
            ]
          },
          {
            id: 'asdadsadsasdaddsad',
            name: 'Pedro 2',
            email: 'p2@sapasd.com',
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

<style lang="scss" scoped>

.md-card.member-card {

  margin-bottom: 2.0em;

  .new-goal-list-item {

    .new-goal-input {
      position: relative;
      top: -10px;
      margin-left: 0px !important;
      max-width: calc(100% - 20px);
    }

    .md-radio.md-theme-default.md-disabled .md-radio-container {
        border-color: rgba(0,0,0,0.26);
        background-color: rgba(0,0,0,0.26);
    }
  }

  .md-list-item-text {
    margin-left: 10px !important;
  }
}

.progress-radio-btn {

  margin-right: 8px;

  .md-radio {
    margin-right: 0px;
  }

  .md-tooltip.md-top {
    margin-left: -5px;
  }
}

</style>
