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

        <form novalidate class="md-layout" @submit.prevent="validateSettings">
          <md-card class="md-layout-item md-size-50 md-small-size-100">
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
                />
                <span class="md-error " v-if="errors.meeting_duration_mins.invalid">
                  Value is invalid. It should be an integer. Example: 13
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
                <span class="md-error " v-if="errors.meeting_link.invalid">
                  Invalid url
                </span>
              </md-field>

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
                <span class="md-error " v-if="errors.slack_webhook.invalid">
                  Invalid url. Url should be start with https://hooks.slack.com/
                </span>
              </md-field>

            </md-card-content>

            <md-card-actions>
              <md-button type="submit" class="md-primary" :disabled="sending">
                Save
              </md-button>
            </md-card-actions>
          </md-card>
        </form>

      </md-app-content>
    </md-app>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data: function() {
    return {
      teamSettings: null,
      errors: {
        meeting_link: {
          invalid: false
        },
        meeting_duration_mins: {
          invalid: false
        },
        slack_webhook: {
          invalid: false
        }
      },
      sending: false
    }
  },
  computed: mapState(['team']),
  created() {
    const res = this.$store.dispatch('getTeam', {
      teamId: this.$route.params.teamId
    });

    res.then(() => {
      this.teamSettings = this.team.settings
    })
  },
  methods: {
    validateSettings() {
      console.log(this.settings);
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
