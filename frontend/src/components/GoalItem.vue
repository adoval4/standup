<template lang="html">
  <md-list-item

  >
    <span class="goal-status-btns">
      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="NOT_DONE"
          class="radio-not-done"
          @change="updateStatus"
        ></md-radio>
        <md-tooltip md-direction="top">Not done</md-tooltip>
      </span>

      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="IN_PROGRESS"
          class="radio-in-progress"
          @change="updateStatus"
        ></md-radio>
        <md-tooltip md-direction="top">In progress</md-tooltip>
      </span>

      <span class="progress-radio-btn">
        <md-radio
          v-model="goal.status"
          value="DONE"
          class="radio-done"
          @change="updateStatus"
        ></md-radio>
        <md-tooltip md-direction="top">Done</md-tooltip>
      </span>

    </span>
    <span class="md-list-item-text">{{ goal.description }}</span>
    <span class="text-muted">{{ daysSince }}</span>
    <md-button class="md-icon-button">
      <md-icon>close</md-icon>
    </md-button>
  </md-list-item>

</template>

<script>
import * as moment from 'moment';

export default {
  props: [
    'memberId',
    'goal'
  ],
  data() {
    return {

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
    }
  },
  methods: {
    updateStatus(value) {

      console.log(value);

      this.$store.dispatch('updateGoalStatus', {
        memberId: this.memberId,
        goalId: this.goal.id,
        status: value
      });
    }
  }
}
</script>

<style lang="scss" scoped>


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


</style>
