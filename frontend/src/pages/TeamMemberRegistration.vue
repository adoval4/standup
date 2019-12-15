<template>
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo">Standup</span>
      </md-app-toolbar>

      <md-app-content >
        <form
          class="md-layout full-height md-alignment-center-center"
          @submit.prevent="sendRequest"
        >
          <md-card class="md-layout-item md-size-30 md-small-size-100 ">
            <md-progress-bar md-mode="indeterminate" v-if="sending" />

            <md-card-header>
              <div class="md-title">You we're inveted to Some team!</div>
            </md-card-header>

            <md-card-content>

              <p>
                Someone invited you to be this team at Standup.

                Standup allows to set the team members' goals and keep up with their progress.
              </p>
              <p>
                Please register yourself to continue.
              </p>

              <md-field >
                <label>Email</label>
                <md-input
                  type="email"
                  :required="true"
                  autocomplete="email"
                  v-model="form.email"
                  :disabled="true"
                />
                <span class="md-error " v-if="form.errors.email.invalid">
                  Email provided is invalid
                </span>
              </md-field>
              <md-field >
                <label>First name</label>
                <md-input
                  type="text"
                  :required="true"
                  v-model="form.first_name"
                  :disabled="sending"
                />
              </md-field>
              <md-field >
                <label>Last name</label>
                <md-input
                  type="text"
                  :required="true"
                  v-model="form.last_name"
                  :disabled="sending"
                />
              </md-field>
              <md-field >
                <label>Password</label>
                <md-input
                  type="password"
                  name="password"
                  id="password"
                  :required="true"
                  v-model="form.password"
                  :disabled="sending"
                />
              </md-field>
              <md-field >
                <label>Password confirmation</label>
                <md-input
                  type="password"
                  name="password"
                  id="password"
                  :required="true"
                  v-model="password_confirmation"
                  :disabled="sending"
                />
              </md-field>
            </md-card-content>

            <md-card-actions>
              <md-button
                type="submit"
                class="md-raised md-primary"
                :disabled="sending"
              >
                Get me in!
              </md-button>
            </md-card-actions>
          </md-card>

        </form>

        <server-unreachable-snackbar></server-unreachable-snackbar>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import ServerUnreachableSnackbar from '../components/ServerUnreachableSnackbar.vue';

export default {
  components: {
    'server-unreachable-snackbar': ServerUnreachableSnackbar,
  },
  data() {
    return {
      teamMemberId: null,
      form: {
        email: null,
        first_name: null,
        last_name: null,
        password: null,
        errors: {
          email: {
            empty: false,
            invalid: false,
          },
          password: {
            empty: false,
          },
        }
      },
      password_confirmation: null,
      sending: false,
    }
  },
  created() {
    this.teamMemberId = this.$route.params.teamMemberId;
  },
  methods: {
    sendRequest() {

    },
    validateForm() {

    },
    isValidEmail: function () {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(this.form.email);
    }
  }
}
</script>

<style lang="scss" scoped>
.md-field .md-error {
    display: block;
    left: 0;
    opacity: 1;
    transform: translate3d(0, 0px, 0);
}

.md-layout-item.md-small-size-100 {
    margin-left: 16px !important;
}
</style>