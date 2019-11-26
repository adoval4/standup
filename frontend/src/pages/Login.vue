<template>
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo">Standup</span>
      </md-app-toolbar>

      <md-app-content >
        <form
          class="md-layout full-height md-alignment-center-center"
          @submit.prevent="validateData"
        >
          <md-card class="md-layout-item md-size-50 md-small-size-100 ">
            <md-progress-bar md-mode="indeterminate" v-if="sending" />

            <md-card-header>
              <div class="md-title">Login</div>
            </md-card-header>
            <md-card-content>
              <md-field >
                <label for="email">Email</label>
                <md-input type="email" name="email" id="email" autocomplete="email" v-model="form.email" :disabled="sending" />
              </md-field>
              <md-field >
                <label for="email">Password</label>
                <md-input type="password" name="email" id="email" autocomplete="email" v-model="form.password" :disabled="sending" />
              </md-field>
              <span class="md-error " v-if="authError">The email or password provided are incorrect</span>
            </md-card-content>



            <md-card-actions>
              <md-button type="submit" class="md-raised md-primary" :disabled="sending">Get me in!</md-button>
            </md-card-actions>
          </md-card>

        </form>
      </md-app-content>
    </md-app>
  </div>
</template>

<style lang="scss" scoped>

  $red-accent: #ff5252;

  .md-app {
    min-height: 100vh;
    height: 100%;
  }

  .md-error {
    color: $red-accent;
  }
</style>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: null,
        password: null
      },
      sending: false,
      authError: false
    }
  },
  methods: {
    validateData() {
      this.sending = true;
      console.log(this.form)
      setTimeout(() => {
        this.authError = true;
        this.sending = false;
      }, 2000)
    }
  }
}
</script>