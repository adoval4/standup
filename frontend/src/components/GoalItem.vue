<template lang="html">
  <md-list-item
    @click.stop
    class="goal-item"
    :md-ripple="false"
    v-if="goal"
  >
    <span class="goal-status-btns">
      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="NOT_DONE"
          class="radio-not-done"
          @change="updateStatus"
          :disabled="editing"
        ></md-radio>
        <md-tooltip md-direction="top">Not done</md-tooltip>
      </span>

      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="IN_PROGRESS"
          class="radio-in-progress"
          @change="updateStatus"
          :disabled="editing"
        ></md-radio>
        <md-tooltip md-direction="top">In progress</md-tooltip>
      </span>

      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="DONE"
          class="radio-done"
          @change="updateStatus"
          :disabled="editing"
        ></md-radio>
        <md-tooltip md-direction="top">Done</md-tooltip>
      </span>

    </span>
    <span
      class="md-list-item-text"
      v-show="!editing"
      @click="editDescription"
    >
      {{ description }}
    </span>
    <span
      class="text-muted"
      v-show="!editing"
    >
      {{ daysSince }}
    </span>
    <md-button
      class="md-icon-button"
      v-show="!editing"
      @click="deleteGoal"
    >
      <md-icon>close</md-icon>
    </md-button>
    <span class="md-list-item-text" v-show="editing">
      <md-field
        class="edit-input"
        md-inline
      >
        <md-input
          v-model="newDescription"
          ref="editionInput"
          :disabled="updating"
          @keyup.enter="updateGoalDescription"
          @blur="updateGoalDescription"
        ></md-input>
      </md-field>

    </span>

  </md-list-item>

</template>

<script>
import * as moment from 'moment';

export default {
  props: [
    'memberId',
    'goalId'
  ],
  data() {
    return {
      editing: false,
      newDescription: null,
      updating: false,
    }
  },
  computed: {
    daysSince: function() {
      if(!this.goal.created) {
        return 'No date'
      }
      let now = moment();
      let days_passed = now.diff(moment(this.goal.created), 'days');
      if(days_passed == 0) {
        return 'Since today'
      }
      return `Since ${days_passed} ${days_passed > 1 ? 'days' : 'day'}`
    },
    goal() {
      return this.$store.state.goals[this.goalId]
    },
    description() {
      return this.updating ? this.newDescription : this.goal.description;
    }
  },
  methods: {
    updateStatus(value) {
      this.$store.dispatch('updateGoalStatus', {
        memberId: this.memberId,
        goalId: this.goal.id,
        status: value
      });
    },
    deleteGoal() {
      this.$store.dispatch('deleteGoal', {
        memberId: this.memberId,
        goalId: this.goal.id
      });
    },
    editDescription() {
      this.newDescription = this.goal.description;
      this.editing = true;

      setTimeout(() => {
        this.$refs['editionInput'].$el.focus();
      }, 100);
    },
    updateGoalDescription() {
      if(this.goal.description === this.newDescription) {
        this.editing = false;
        return;
      }

      this.updating = true;
      this.$store.dispatch('updateGoalDescription', {
        memberId: this.memberId,
        goalId: this.goal.id,
        description: this.newDescription
      });
      this.editing = false;

      setTimeout(() => { this.updating = false; }, 500)
    }
  }
}
</script>

<style lang="scss" scoped>

.md-list-item.goal-item {

  .md-list-item-text {
    margin-left: 10px !important;
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
}

.edit-input {
  position: relative;
  top: -10px;
  margin-left: 0px !important;
  max-width: calc(100% - 20px);
}


.md-list.md-theme-default .md-list-item-container:not(.md-list-item-default):not(.md-list-item-expand):not([disabled]) {
  background-color: transparent !important;
  color: inherit !important;
}


</style>
