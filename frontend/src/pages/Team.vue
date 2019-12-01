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

      <md-app-content class="md-scrollbar">
        <md-progress-bar
          md-mode="indeterminate"
          v-if="!team"
        >
        </md-progress-bar>

        <member-to-do-list
          v-for="member in team.members"
          :member="member"
          class="member-card"
        >
        </member-to-do-list>

        <md-card
          class=""
        >

          <md-card-header>
            <div class="md-title">+ New member</div>
            <!-- <div class="md-subhead">+ New member</div> -->
          </md-card-header>
          <form novalidate @submit.prevent="validateNewMember">
            <md-card-content >
              <div class="md-layout md-gutter">
                <div class="md-layout-item md-small-size-50">
                  <md-field
                    class=""
                    md-inline
                  >
                    <label>Name</label>
                    <md-input
                      name="new-member-name"
                      id="new-member-name"
                      v-model="newMember.name"
                      :disabled="newMember.sending"
                    ></md-input>
                  </md-field>
                </div>
                <div class="md-layout-item md-small-size-50">
                  <md-field
                    class=""
                    md-inline
                  >
                    <label>Email</label>
                    <md-input
                      name="new-member-email"
                      id="new-member-email"
                      v-model="newMember.email"
                      :disabled="newMember.sending"
                    ></md-input>
                  </md-field>
                </div>

              </div>
            </md-card-content>

            <md-card-actions>
              <md-button
                type="submit"
                class="md-primary"
                :disabled="newMember.sending"
              >
                Add
              </md-button>
            </md-card-actions>
          </form>
        </md-card>



      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import MemberToDoList from '../components/MemberToDoList.vue';

export default {
  components: {
    'member-to-do-list': MemberToDoList
  },
  data: function() {
    return {
      newMember: {
        name: null,
        email: null,
        sending: false
      },
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
  },
  methods: {
    validateNewMember() {
      console.log(this.newMember);
    }
  }
}
</script>

<style lang="scss" scoped>

.md-card.member-card {

  margin-top: 1.5em;
  margin-bottom: 2.5em;

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
