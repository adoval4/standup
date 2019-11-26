<template lang="html">
  <div class="">
    Team {{team_id}}
    <router-link :to="{ name: 'teamSettings', params:{teamId: this.team_id} }">
      Settings
    </router-link>
    <router-link :to="{ name: 'home' }">
      Back home
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
