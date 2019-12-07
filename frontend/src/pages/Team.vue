<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <md-button v-if="user" class="md-icon-button" :to="{ name: 'home' }">
          <md-icon>arrow_back</md-icon>
        </md-button>
        <span v-if="team" class="md-title logo" style="flex: 1">
          Standup - {{ team.name }}
        </span>
        <md-button v-if="team && isTeamManager" @click="callTeam">Call</md-button>
        <timer-button v-if="team && isTeamManager">Call</timer-button>
        <md-button
          v-if="team && isTeamManager"
          :to="{ name: 'teamSettings', payload:{ teamId: this.team.id } }"
          class="md-icon-button"
        >
					<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <path
              style="fill: #fff;"
              d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"
            />
          </svg>
        </md-button>
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
          :key="member.id"
          class="member-card"
        >
        </member-to-do-list>

        <md-card
          v-if="isTeamManager"
          class="member-card new-member-card"
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

        <a
          id="meeting-link-btn"
          v-if="team"
          :href="team.settings.meeting_link"
          target="_blank"
          rel="noopener noreferrer"
          v-show="false"
        >
        </a>

        <md-snackbar
          md-position="left"
          :md-duration="2500"
          :md-active.sync="showCalledTeamSnackbar"
          md-persistent
        >
          <span>Team called successfully!</span>
        </md-snackbar>

        <md-snackbar
          md-position="left"
          :md-duration="4500"
          :md-active.sync="showCalledTeamFailedSnackbar"
          md-persistent
        >
          <span>Error: Calling team failed</span>
        </md-snackbar>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import MemberToDoList from '../components/MemberToDoList.vue';
import TimerButton from '../components/TimerButton.vue';
import { mapState } from 'vuex';

export default {
  components: {
    'member-to-do-list': MemberToDoList,
    'timer-button': TimerButton
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
      },
      showCalledTeamSnackbar: false,
      showCalledTeamFailedSnackbar: false,
    }
  },
  computed: {
    user() { return this.$store.state.user },
    team() { return this.$store.state.team },
    isTeamManager() { return this.$store.getters.isUserTeamManager },
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
    callTeam: function() {
      const res = this.$store.dispatch('callTeam');
      // open metting link is available
      res.then(() => {
        this.showCalledTeamSnackbar = true;
        this.openMeetingLink()
      }).catch(() => {
        this.showCalledTeamFailedSnackbar = true;
      })
    },
    openMeetingLink: function() {
      if(!this.team.settings.meeting_link) { return; }
      const meeting_a_tag = document.getElementById('meeting-link-btn');
      meeting_a_tag.click();
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

.md-card.member-card.new-member-card {
  margin-top: 1.5em;
  margin-bottom: 2.5em;
  padding-bottom: 1.5em;
}

</style>
