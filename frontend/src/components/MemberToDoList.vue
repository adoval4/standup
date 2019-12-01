<template lang="html">
  <md-card
    class="member-card"
  >
    <md-card-header>
      <div class="md-title">{{ member.name }}</div>
      <div class="md-subhead">{{ member.email }}</div>
    </md-card-header>

    <md-card-content >
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

</template>

<script>
export default {
  props: [
    'member'
  ]
}
</script>

<style lang="css" scoped>
</style>
