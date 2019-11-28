<template>
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <span class="md-title logo">Standup</span>
      </md-app-toolbar>

      <md-app-content >
        <form
          class="md-layout full-height md-alignment-center-center"
          :class="{ 'md-invalid': !isFormValid }"
          @submit.prevent="validateData"
        >
          <md-card class="md-layout-item md-size-30 md-small-size-100 ">
            <md-progress-bar md-mode="indeterminate" v-if="sending" />

            <md-card-header>
              <div class="md-title">Login</div>
            </md-card-header>

            <md-card-content>
              <md-field >
                <label for="email">Email</label>
                <md-input
                  type="email"
                  name="email"
                  id="email"
                  :required="true"
                  autocomplete="email"
                  v-model="form.email"
                  :disabled="sending"
                />
                <span class="md-error " v-if="form.errors.email.invalid">
                  Email provided is invalid
                </span>
              </md-field>
              <md-field >
                <label for="email">Password</label>
                <md-input
                  type="password"
                  name="password"
                  id="password"
                  :required="true"
                  autocomplete="password"
                  v-model="form.password"
                  :disabled="sending"
                />
              </md-field>
              <span class="md-error " v-if="authError">
                The email or password provided are incorrect
              </span>
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
      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import ApiClient from '../services/api_client'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        email: null,
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
      isFormValid: true,
      sending: false,
      authError: false
    }
  },
  methods: {
    validateData: function() {
      if(!this.validateForm()) {
        return;
      }

      this.sending = true;

      let res = ApiClient.auth(
        this.form.email,
        this.form.password
      );

      console.log(res)

      res.then((response) => {
        this.$store.commit('setUser', {'user': response.data})
        this.$router.push({ name: 'home' })
      }).catch((error) => {
        console.log(error);
        this.authError = true;
      }).finally(() => {
        this.sending = false;
      });

    },
    validateForm() {
      let isValid = true;
      this.authError = false;
      this.isFormValid = isValid;
      // reset errors
      this.$set(this.form, 'errors', {
        email: {
          empty: false,
          invalid: false,
        },
        password: {
          empty: false,
        },
      });

      if(!this.form.email) {
        this.$set(this.form.errors.email, 'empty', true);
        isValid = false;
      }
      else if(!this.isValidEmail()) {
        this.$set(this.form.errors.email, 'invalid', true);
        isValid = false;
      }

      if(!this.form.password) {
        this.$set(this.form.errors.password, 'empty', true);
        isValid = false;
      }

      this.isFormValid = isValid;
      return isValid;
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
</style>