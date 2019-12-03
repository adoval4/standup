<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <md-button class="md-icon-button" :to="{ name: 'home' }">
          <md-icon>arrow_back</md-icon>
        </md-button>
        <span v-if="team" class="md-title logo">
          Standup - {{ team.name }}
        </span>
      </md-app-toolbar>

      <md-app-content v-if="team" class="md-scrollbar">
        <md-progress-bar
          md-mode="indeterminate"
          v-if="!team"
        >
        </md-progress-bar>

        <member-to-do-list

          v-for="member in team.members"
          :member="member"
          class="member-card"
        >
        </member-to-do-list>

        <md-card
          class="member-card"
        >
          <md-progress-bar
            v-if="newMember.sending"
            md-mode="indeterminate"
          >
          </md-progress-bar>
          <md-card-header>
            <div v-if="team.members.length > 0" class="md-title">+ New member</div>
            <div v-if="team.members.length == 0" class="md-title">+ Add first member</div>
          </md-card-header>
          <form novalidate @submit.prevent="createNewMember">
            <md-card-content class="new-memeber-form-ctn" >
              <div class="md-layout md-gutter">
                <div class="md-layout-item md-small-size-50">
                  <md-field
                    class=""
                    md-inline
                  >
                    <label>Name</label>
                    <md-input
                      name="new-member-name"
                      id="new-member-name"
                      v-model="newMember.name"
                      :disabled="newMember.sending"
                    ></md-input>
                    <span class="md-error " v-if="newMember.errors.name.empty">
                      Name is required
                    </span>
                  </md-field>
                </div>
                <div class="md-layout-item md-small-size-50">
                  <md-field
                    class=""
                    md-inline
                  >
                    <label>Email</label>
                    <md-input
                      name="new-member-email"
                      id="new-member-email"
                      v-model="newMember.email"
                      :disabled="newMember.sending"
                    ></md-input>
                    <span class="md-error " v-if="newMember.errors.email.empty">
                      Email is required
                    </span>
                    <span class="md-error " v-if="newMember.errors.email.invalid">
                      Email provided is invalid
                    </span>
                    <span class="md-error " v-if="newMember.errors.email.existing">
                      Email is already registered on this team
                    </span>
                  </md-field>
                </div>
              </div>
            </md-card-content>

            <md-card-actions>
              <md-button
                type="submit"
                class="md-primary"
                :disabled="newMember.sending"
              >
                Add
              </md-button>
            </md-card-actions>
          </form>
        </md-card>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import MemberToDoList from '../components/MemberToDoList.vue';

export default {
  components: {
    'member-to-do-list': MemberToDoList
  },
  data: function() {
    return {
      newMember: {
        name: null,
        email: null,
        sending: false,
        errors: {
          email: {
            empty: false,
            invalid: false,
            existing: false
          },
          name: {
            empty: false,
          },
        }
      }
    }
  },
  computed: {
    team() {
      return this.$store.state.team;
    }
  },
  created() {
    this.$store.dispatch('getTeam', {
      teamId: this.$route.params.teamId
    });
  },
  methods: {
    createNewMember() {
      if(!this.validateNewMember()) { return; }

      this.$set(this.newMember, 'sending', true);

      this.$store.dispatch('createTeamMember', {
        name: this.newMember.name,
        email: this.newMember.email
      });

      this.$set(this.newMember, 'name', null);
      this.$set(this.newMember, 'email', null);
      this.$set(this.newMember, 'sending', false);
    },
    validateNewMember() {
      let isValid = true;
      this.$set(this.newMember, 'errors', {
        email: {
          empty: false,
          invalid: false,
          existing: false
        },
        name: {
          empty: false,
        },
      });

      if(!this.newMember.email) {
        this.$set(this.newMember.errors.email, 'empty', true);
        isValid = false;
      }
      else if(!this.isValidEmail(this.newMember.email)) {
        this.$set(this.newMember.errors.email, 'invalid', true);
        isValid = false;
      }

      if(!this.newMember.name) {
        this.$set(this.newMember.errors.name, 'empty', true);
        isValid = false;
      }

      return isValid;
    },
    isValidEmail: function (email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
  }
}
</script>

<style lang="scss" scoped>

.new-memeber-form-ctn {
  margin-right: 15px;
  margin-left: 20px;
}

</style>
