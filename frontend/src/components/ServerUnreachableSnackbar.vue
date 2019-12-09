<template lang="html">
  <div class="">
    <md-snackbar
      class="md-accent"
      md-position="center"
      :md-duration="1000"
      :md-active="isServerUnreachable"
      md-persistent
    >
      <span>Error: Server unreachable!</span>
    </md-snackbar>
  </div>
</template>

<script>
export default {
  computed: {
    isServerUnreachable() {
      return !this.$store.state.isServerRechable;
    }
  }
}
</script>

<style lang="css" scoped>
</style>
