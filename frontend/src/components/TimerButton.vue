<template lang="html">
  <div class="timer-button-ctn">
    <md-button
      v-show="!finished"
      class="md-dense"
      v-bind:class="{
        'md-primary': !running,
        'on-time': (running && !time_is_over),
        'out-of-time': (running && time_is_over)
      }"
      :md-riple="false"
      @click="timerToggle"
     >
      <span v-show="!wasStarted" class="label">
        <md-icon>play_arrow</md-icon> Start {{ time_left_str }}
      </span>
      <span v-show="wasStarted && !running && !finished" class="label">
        <md-icon>play_arrow</md-icon> Resume {{ time_left_str }}
      </span>
      <span v-show="wasStarted && running && !finished" class="label">
        <md-icon>pause</md-icon> Pause {{ time_left_str }}
      </span>
    </md-button>
    <md-button
      class="md-dense"
      :class="{
        'finish': !finished,
        'finished': finished
      }"
      v-if="wasStarted && !running"
      :disabled="finished"
      @click="setAsFinish"
    >
      We are done<span v-show="!finished"> ?</span><span v-show="finished"> !!</span>
    </md-button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      time_passed_ms: 0,
      wasStarted: false,
      finished: false,
      running: false,
      interval_ms: 20,
      title: 'Start'
    }
  },
  computed: {
    team() { return this.$store.state.team },
    time_left_str: function() {
      if(!this.team.settings.meeting_duration_mins) {
        return '---';
      }
      const metting_time_ms = this.team.settings.meeting_duration_mins;
      const time_left = metting_time_ms * 60 * 1000 - this.time_passed_ms;
      const sign = time_left >= 0 ? '' : '-';
      const time_left_abs = Math.abs(time_left);
      const minutes = Math.floor(time_left_abs/60/1000);
      const seconds = Math.floor(time_left_abs/1000) - minutes * 60;

      const minutes_str = minutes >= 10 ? minutes : `0${minutes}`;
      const seconds_str = seconds >= 10 ? seconds : `0${seconds}`;

      return `${sign}${minutes_str}:${seconds_str}`;
    },
    time_is_over: function() {
      return this.total_time_ms - this.time_passed_ms <= 0;
    }
  },
  mounted: function() {
    setInterval(()=>{
      if(this.running) {
        this.time_passed_ms += this.interval_ms;
      }
    }, this.interval_ms);
  },
  methods: {
    timerToggle: function() {
      this.wasStarted = true;
      this.running = !this.running;
    },
    setAsFinish: function() {
      const res = this.$store.dispatch('archiveGoalsDone');
      res.then(() => {
        this.finished = true;        
      })
    }
  }
}
</script>

<style lang="scss" scoped>

.timer-button-ctn {
  margin-right: 1.5em;
}

span.label {

  position: relative;
  top: 2px;

  .md-icon {
    position: relative;
    top: -2px;
  }
}

button.md-button.on-time {
    background: #1a6eff;
}

button.md-button.out-of-time {
    background: #ff5252;
}

button.md-button.finish {
    background: #29c23d;
}

button.md-button.finished {
  color: #fff;
  animation: blinker 2s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}

</style>
