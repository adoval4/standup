<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'app',
  created(){
    this.$store.commit('retrieveUserFromLocalStorage');
  }
}
</script>

<style lang="scss">
@import './scss/main.scss';


</style>
