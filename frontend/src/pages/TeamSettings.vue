<template lang="html">
  <div class="">
    Team settings {{team_id}}
    <router-link :to="{ name: 'team', params:{teamId: this.team_id} }">
      Back to team
    </router-link>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      team_id: null
    }
  },
  created() {
    this.team_id = this.$route.params.teamId;
  }
}
</script>

<style lang="css" scoped>
</style>
