<template>
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo">Standup</span>
      </md-app-toolbar>

      <!-- Case when the memeber has no user -->
      <md-app-content
        v-if="member && memberHasNoUser"
      >
        <form
          class="md-layout full-height md-alignment-center-center"
          @submit.prevent="sendRequest"
        >
          <md-card class="md-layout-item md-size-30 md-small-size-100 ">
            <md-progress-bar md-mode="indeterminate" v-if="sending" />

            <md-card-header>
              <div class="md-title">You we're inveted to {{ member.team.name }}!</div>
            </md-card-header>

            <md-card-content>

              <p>
                {{ member.created_by.first_name }} {{ member.created_by.last_name }} invited you to join this team at Standup.
              </p>
              <p>
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
                <span class="md-helper-text">
                  This the email where the invitation was sent. Can't be modified.
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
                <span class="md-error" v-if="form.errors.first_name.empty">This is required</span>
              </md-field>
              <md-field >
                <label>Last name</label>
                <md-input
                  type="text"
                  :required="true"
                  v-model="form.last_name"
                  :disabled="sending"
                />
                <span class="md-error" v-if="form.errors.last_name.empty">This is required</span>
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
                <span class="md-helper-text">
                  Make it at least 8 characters long.
                </span>
              </md-field>
              <span class="md-error" v-if="form.errors.password.empty">This is required</span>
              <span class="md-error" v-if="form.errors.password.invalid">This password is too short</span>

              <md-field >
                <label>Password confirmation</label>
                <md-input
                  type="password"
                  name="password"
                  id="password-confirmation"
                  :required="true"
                  v-model="password_confirmation"
                  :disabled="sending"
                />
                <span class="md-error" v-if="form.password && !password_confirmation_is_valid">
                  This password is different to the one above.
                </span>
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

        <md-dialog-confirm
          :md-active.sync="showSuccessDialog"
          md-title="Success!"
          md-content="You have registered successfully. Now, please login to continue."
          md-confirm-text="Go to login"
          md-cancel-text=""
          @md-confirm="goToLogin"
        />

      </md-app-content>

      <!-- Case when the memeber already has user -->
      <md-app-content
        v-if="member && !memberHasNoUser"
      >
        <div class="full-height md-alignment-center-center text-center">
          <p class="md-display-2 not-transparent">
            🎉
          </p>
          <p class="md-title">
            You have already registered!
          </p>
          <router-link to="/">
            Go home
          </router-link>
        </div>
      </md-app-content>

      <!-- Case when the memeber already has user -->
      <md-app-content
        v-if="!member && errorResponse && errorResponse.status == 404"
      >
        <div class="full-height md-alignment-center-center text-center">
          <p class="md-display-2 not-transparent">
            🤔
          </p>
          <p class="md-title">
            Nothing to do here
          </p>
          <router-link to="/">
            Go home
          </router-link>
        </div>
      </md-app-content>

      <server-unreachable-snackbar></server-unreachable-snackbar>
    </md-app>
  </div>
</template>

<script>
import ServerUnreachableSnackbar from '../components/ServerUnreachableSnackbar.vue';

const MIN_PASSWORD_LENGTH = 8;

export default {
  components: {
    'server-unreachable-snackbar': ServerUnreachableSnackbar,
  },
  data() {
    return {
      teamId: null,
      teamMemberId: null,
      member: null,
      errorResponse: null,
      showSuccessDialog: false,
      form: {
        email: null,
        first_name: null,
        last_name: null,
        password: null,
        errors: {
          first_name: {
            empty: false,
          },
          last_name: {
            empty: false,
          },
          password: {
            empty: false,
            invalid: false,
          },
        }
      },
      password_confirmation: null,
      sending: false,
    }
  },
  computed: {
    memberHasNoUser() {
      if(!this.member) { return false }
      return !this.member.user
    },
    password_confirmation_is_valid() {
      if(!this.password_confirmation) { return false }
      return this.password_confirmation == this.form.password;
    }
  },
  created() {
    this.teamId = this.$route.params.teamId;
    this.teamMemberId = this.$route.params.teamMemberId;

    const res = this.$store.dispatch('getTeamMember', {
      teamId: this.teamId,
      teamMemberId: this.teamMemberId
    });

    res.then((response) => {
      this.member = response.data;
      this.$set(this.form, 'email', this.member.email)
    }).catch((error) => {
      if(!error.response) { return; }
      this.errorResponse = error.response;
    })
  },
  methods: {
    sendRequest() {
      const isValid = this.validateForm();
      if(!isValid) { return }

      this.sending = true;
      const res = this.$store.dispatch('createUser', {
        email: this.form.email,
        first_name: this.form.first_name,
        last_name: this.form.last_name,
        password: this.form.password
      });

      res.then((response) => {
        this.showSuccessDialog = true
      }).catch((error) => {
        if(!error.response) { return; }
        this.errorResponse = error.response;
      }).finally(() => {
        this.sending = false;
      })
    },
    validateForm() {
      let isValid = true;
      this.$set(this.form, 'errors', {
        first_name: {
          empty: false,
        },
        last_name: {
          empty: false,
        },
        password: {
          empty: false,
          invalid: false,
        },
      });

      if(!this.form.first_name) {
        this.$set(this.form.errors.first_name, 'empty', true);
        isValid = false;
      }
      if(!this.form.last_name) {
        this.$set(this.form.errors.last_name, 'empty', true);
        isValid = false;
      }
      if(!this.form.password) {
        this.$set(this.form.errors.password, 'empty', true);
        isValid = false;
      }
      else if(this.form.password.length < MIN_PASSWORD_LENGTH) {
        console.log('hey')
        this.$set(this.form.errors.password, 'invalid', true);
        isValid = false;
      }

      return isValid && this.password_confirmation_is_valid;
    },
    isValidEmail: function () {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(this.form.email);
    },
    goToLogin() {
      this.$router.push('/login')
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

.not-transparent {
  color: #000;
}
</style>