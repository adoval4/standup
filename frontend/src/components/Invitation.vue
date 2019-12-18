<template lang="html">
  <md-list-item>
    <span
      class="md-list-item-text"
      style="flex: 1;"
    >
      {{ invitation.created_by.first_name }} {{ invitation.created_by.last_name }} has invited you to {{ invitation.team.name }}
    </span>
    <md-button
      class="md-button md-primary"
      @click="acceptInvitation"
    >
      Aceptar
    </md-button>
    <md-button
      class="md-button text-muted"
      @click="declineInvitation"
    >
      Declinar
    </md-button>

  </md-list-item>
</template>

<script>
export default {
  props: [
    'invitation'
  ],
  methods: {
    acceptInvitation() {

    },
    declineInvitation() {

    },
  }
}
</script>

<style lang="scss" scoped>
</style>
