<template lang="html">
  <div class="">
    Home
    <router-link :to="{ name: 'login' }">
      Login
    </router-link>
    <router-link :to="{ name: 'team', params: {teamId: 12312312} }">
      Team
    </router-link>
    <a @click="logoutUser" href="#">
      Logout
    </a>
    <div class="">
      {{ user }}
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    user: function() {
      return this.$store.state.user;
    }
  },
  methods: {
    logoutUser: function() {
      this.$store.commit('logoutUser');
    }
  }
}
</script>

<style lang="css" scoped>
</style>
