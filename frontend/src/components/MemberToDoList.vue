<template lang="html">
  <div class="">

    <md-card
      class="member-card"
    >
      <md-progress-bar
        v-if="newGoal.sending"
        md-mode="indeterminate"
      >
      </md-progress-bar>

      <div class="md-layout">
        <md-card-header class="md-layout-item">
          <div class="md-title">
            {{ member.name }}
            <span v-if="!member.user">
              <md-icon class="md-accent">warning</md-icon>
              <md-tooltip md-direction="top">Hasn't registered yet!</md-tooltip>
            </span>
          </div>
          <div class="md-subhead">{{ member.email }}</div>
        </md-card-header>

        <md-card-actions
          v-if="isTeamManager"
          class="md-layout-item"
        >
          <md-button
            v-if="!member.user"
            @click="resendInvitationEmail"
          >
            Reenviar invitación
          </md-button>
          <md-button
            class="md-icon-button"
            @click="showDeleteConfirmation = true"
          >
            <md-icon>delete</md-icon>
          </md-button>
        </md-card-actions>
      </div>

      <md-card-content >
        <md-list>
          <goal-item
            v-for="goal in member.goals"
            :goalId="goal.id"
            :memberId="member.id"
            :key="goal.id"
          >
          </goal-item>

          <md-list-item v-if="member.goals.length == 0" class="text-muted">
            No pending goals for now
          </md-list-item>

          <md-list-item
            v-if="isTeamManager"
            class="new-goal-list-item"
          >
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
                <md-input
                  v-model="newGoal.description"
                  :disabled="newGoal.sending"
                  @keyup.enter="createNewGoal"
                ></md-input>
              </md-field>
            </span>
          </md-list-item>

        </md-list>
      </md-card-content>
    </md-card>

    <md-dialog-confirm
      v-if="isTeamManager"
      :md-active.sync="showDeleteConfirmation"
      md-title="Are you sure?"
      :md-content="`Please confirm you want to remove ${this.member.name} from this team.`"
      md-confirm-text="Cancel"
      md-cancel-text="Delete"
      @md-cancel="deleteMember"
      @md-confirm="showDeleteConfirmation = false"
    />

    <md-snackbar
      md-position="left"
      :md-duration="4500"
      :md-active.sync="showResendInvitationSnackbar"
      md-persistent
    >
      <span>Invitation sent!</span>
    </md-snackbar>

  </div>

</template>

<script>
import GoalItem from './GoalItem.vue'

export default {
  components: {
    'goal-item': GoalItem
  },
  props: [
    'member'
  ],
  data() {
    return {
      newGoal: {
        description: null,
        sending: false
      },
      showDeleteConfirmation: false,
      showResendInvitationSnackbar: false
    }
  },
  computed: {
    isTeamManager() { return this.$store.getters.isUserTeamManager },
    team() { return this.$store.state.team },
  },
  methods: {
    createNewGoal() {
      this.$set(this.newGoal, 'sending', true);

      this.$store.dispatch('createNewMemberGoal', {
        memberId: this.member.id,
        description: this.newGoal.description
      });

      this.$set(this.newGoal, 'description', null);
      this.$set(this.newGoal, 'sending', false);
    },
    deleteMember() {
      this.$store.dispatch('deleteMember', {
        memberId: this.member.id
      });
    },
    resendInvitationEmail() {
      const res = this.$store.dispatch('resendMemberInvitation', {
        teamId: this.team.id,
        teamMemberId: this.member.id
      });

      res.then(() => {
        this.showResendInvitationSnackbar = true;
      })
    }
  }
}
</script>

<style lang="scss" scoped>

.md-card.member-card {
  margin-top: 1.5em;
  margin-bottom: 2.5em;
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

.new-goal-list-item {

  .new-goal-input {
    position: relative;
    top: -10px;
    margin-left: 10px !important;
    max-width: calc(100% - 30px);
  }

  .md-radio.md-theme-default.md-disabled .md-radio-container {
      border-color: rgba(0,0,0,0.26);
      background-color: rgba(0,0,0,0.26);
  }
}


</style>
