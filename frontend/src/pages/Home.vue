<template lang="html">
  <div class="">
    Home
    <router-link :to="{ name: 'login' }">
      Login
    </router-link>
    <router-link :to="{ name: 'team', params: {teamId: 12312312} }">
      Team
    </router-link>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css" scoped>
</style>
