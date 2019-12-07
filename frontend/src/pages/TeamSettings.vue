<template lang="html">
  <div class="page-container">
    <md-app md-waterfall md-mode="fixed">
      <md-app-toolbar class="md-primary">
        <md-button
          v-if="team"
          class="md-icon-button"
          :to="{ name: 'team', payload:{ teamId: this.team.id } }"
        >
          <md-icon>arrow_back</md-icon>
        </md-button>
        <span v-if="team" class="md-title logo">
          Standup - {{ team.name }} | Settings
        </span>
      </md-app-toolbar>
      <md-app-content v-if="teamSettings" class="md-scrollbar">

        <form novalidate class="md-layout" @submit.prevent="updateSettings">
          <md-card class="md-layout-item md-size-50 md-small-size-100">
            <md-progress-bar md-mode="indeterminate" v-if="sending" />

            <md-card-header>
              <div class="md-title">Team meeting settings</div>
            </md-card-header>

            <md-card-content>

              <md-field>
                <label>Meeting duration in minutes</label>
                <md-input
                  v-model="teamSettings.meeting_duration_mins"
                  :disabled="sending"
                  :required="true"
                  type="number"
                />
                <span class="md-error " v-if="errors.meeting_duration_mins.empty">
                  This is required.
                </span>
                <span class="md-error " v-if="errors.meeting_duration_mins.invalid">
                  Value is invalid. It should be an integer. Example: 13.
                </span>
              </md-field>

              <md-field>
                <label>Call url</label>
                <md-input
                  v-model="teamSettings.meeting_link"
                  :disabled="sending"
                />
                <span class="md-helper-text">
                  Video call where the meeting will be held. Whenever you call your team, a tab with this url will be open.
                </span>
              </md-field>
              <span class="md-error " v-if="errors.meeting_link.invalid">
                Invalid url
              </span>

              <div class="radio-field">
                <span class="label">Call team by:</span>
                <div class="">
                  <md-radio
                    v-model="teamSettings.call_team_method"
                    value="EMAIL"
                  >
                    Email
                  </md-radio>
                  <md-radio
                    v-model="teamSettings.call_team_method"
                    value="SLACK"
                  >
                    Slack
                  </md-radio>
                </div>
              </div>

              <md-field v-show="teamSettings.call_team_method == 'SLACK'">
                <label for="email">Slack webhook url</label>
                <md-input
                  v-model="teamSettings.slack_webhook"
                  :disabled="sending"
                />
                <span class="md-helper-text">
                  Slack incoming webhook allow you to send messages to a specific Slack channel.
                  <a href="https://api.slack.com/messaging/webhooks">See more</a>
                </span>
              </md-field>
              <span class="md-error " v-if="errors.slack_webhook.empty">
                If you are gonna be using slack to call your team, this is required.
              </span>
              <span class="md-error " v-if="errors.slack_webhook.invalid">
                Invalid url. A valid url should start with "https://hooks.slack.com/".
              </span>

            </md-card-content>

            <md-card-actions>
              <md-button type="submit" class="md-primary" :disabled="sending">
                Save
              </md-button>
            </md-card-actions>
          </md-card>
        </form>

        <md-button
          @click="showDeleteConfimation = true"
          class="md-accent"
        >
          Delete this team
        </md-button>


        <md-dialog-confirm
          v-if="showDeleteConfimation"
          :md-active.sync="showDeleteConfimation"
          md-title="Are you sure?"
          :md-content="`Please confirm you want to delete this team.`"
          md-confirm-text="Cancel"
          md-cancel-text="Delete"
          @md-cancel="deleteTeam"
          @md-confirm="showDeleteConfimation = false"
        />


        <md-snackbar
          md-position="left"
          :md-duration="2500"
          :md-active.sync="showUpdateSnackbar"
          md-persistent
        >
          <span>Successful update!</span>
        </md-snackbar>



      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import { mapState } from 'vuex';

const SLACK_WEBHOOK_ROOT = '//hooks.slack.com/';

export default {
  data: function() {
    return {
      teamSettings: null,
      errors: {
        meeting_link: {
          invalid: false
        },
        meeting_duration_mins: {
          invalid: false,
          empty: false
        },
        slack_webhook: {
          invalid: false
        }
      },
      sending: false,
      showDeleteConfimation: false,
      showUpdateSnackbar: false
    }
  },
  computed: mapState(['team']),
  mounted() {
    if(!this.team){
      const res = this.$store.dispatch('getTeam', {
        teamId: this.$route.params.teamId
      });
      res.finally(() => { this.teamSettings = this.team.settings; })
    } else {
      this.teamSettings = this.team.settings;
    }
  },
  methods: {
    validateSettings() {
      let isValid = true;
      if(!this.teamSettings) { return false }

      this.errors = {
        meeting_link: {
          invalid: false
        },
        meeting_duration_mins: {
          invalid: false,
          empty: false
        },
        slack_webhook: {
          empty: false,
          invalid: false,
        }
      };

      if(!this.teamSettings.meeting_duration_mins) {
        this.$set(this.errors.meeting_duration_mins, 'empty', true)
        isValid = false;
      }
      else{
        const parsedValue = parseInt(this.teamSettings.meeting_duration_mins, null);
        if(!parsedValue) {
          this.$set(this.errors.meeting_duration_mins, 'invalid', true)
          isValid = false;
        }
        else {
          this.$set(this.teamSettings, 'meeting_duration_mins', parsedValue)
        }
      }

      if(this.teamSettings.meeting_link &&
        !this.validateURL(this.teamSettings.meeting_link)
      ) {
        this.$set(this.errors.meeting_link, 'invalid', true)
        isValid = false;
      }

      if(this.teamSettings.call_team_method == 'SLACK'){
        if(!this.teamSettings.slack_webhook) {
          this.$set(this.errors.slack_webhook, 'empty', true)
          isValid = false;
        }
        else if(!this.validateURL(this.teamSettings.slack_webhook)){
          this.$set(this.errors.slack_webhook, 'invalid', true)
          isValid = false;
        }
        else if(!this.validateSlackWebhook(this.teamSettings.slack_webhook)){
          this.$set(this.errors.slack_webhook, 'invalid', true)
          isValid = false;
        }
      }
      return isValid;
    },
    validateURL(str)
    {
      let re =  /^(?:(?:https?|ftp):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$/;
      return re.test(str)
    },
    validateSlackWebhook(str)
    {
      return str.indexOf(SLACK_WEBHOOK_ROOT) > 0;
    },
    updateSettings() {
      if(!this.validateSettings()) {
        return;
      }

      this.sending = true;

      const res = this.$store.dispatch('updateTeamSettings', {
        settings: this.teamSettings
      })

      res.then(() => {
        this.showUpdateSnackbar = true;
      }).finally(() => {
        this.sending = false;
      })
    },

    deleteTeam: function() {
      if(!this.team) { return }

      this.$store.dispatch('deleteTeam', {
        teamId: this.team.id
      })

      this.$router.push('/')
    }

  }
}
</script>

<style lang="scss" scoped>

.radio-field {

  padding-top: 30px;

  .label {
    color: rgba(0,0,0,0.54);
    font-size: 16px;
    line-height: 20px;
  }

  .md-radio {
    margin-top: 10px;
    margin-bottom: 12px;
  }

}

</style>
