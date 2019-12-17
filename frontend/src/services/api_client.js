import axios from 'axios';


const baseUrl = process.env.API_URL;
const apiBaseUrl = `${baseUrl}/api/v1`;
const userListUrl = `${apiBaseUrl}/users/`;
const myInfoUrl = `${userListUrl}me/`;
const teamListUrl = `${apiBaseUrl}/teams/`;
const goalsListUrl = `${apiBaseUrl}/goals/`;

const StandupApiClient = {

  auth: function(email, password) {
    const authUrl = `${baseUrl}/api-token-auth/`;
    return axios.post(authUrl, {username: email, password: password})
  },

  getOptions: function(token) {
    if(!token) { return {} }
    return { headers: { 'Authorization': `Token ${token}` } };
  },

  getMyInfo: function(token) {
    return axios.get(myInfoUrl, this.getOptions(token));
  },

  getTeams: function(token) {
    return axios.get(teamListUrl, this.getOptions(token));
  },

  retrieveTeam: function(token = null, teamId) {
    const teamDetailUrl = `${teamListUrl}${teamId}/`;
    return axios.get(teamDetailUrl, this.getOptions(token));
  },

  createTeam: function(token, newTeamName) {
    const data = { name: newTeamName }
    return axios.post(
      teamListUrl,
      data,
      this.getOptions(token)
    );
  },

  deleteTeam: function(token, teamId) {
    const teamDetailUrl = `${teamListUrl}${teamId}/`;
    return axios.delete(teamDetailUrl, this.getOptions(token));
  },

  createTeamMember: function(token, teamId, newMemberName, newMemberEmail) {
    const teamMembersUrl = `${teamListUrl}${teamId}/members/`;
    const data = {
      name: newMemberName,
      email: newMemberEmail
    }
    return axios.post(teamMembersUrl, data, this.getOptions(token));
  },

  createMemberGoal: function(token, memberId, newGoalDescription) {
    const data = {
      member: memberId,
      description: newGoalDescription
    }
    return axios.post(goalsListUrl, data, this.getOptions(token));
  },

  updateTeamSettings: function(token, teamId, newSettings) {
    const teamSettingsUrl = `${teamListUrl}${teamId}/setup/`;
    return axios.put(teamSettingsUrl, newSettings, this.getOptions(token));
  },

  updateGoalStatus: function(token = null, goalId, status) {
    const goalDetailUrl = `${goalsListUrl}${goalId}/`;
    const data = { status };
    return axios.patch(goalDetailUrl, data, this.getOptions(token));
  },

  updateGoalDescription: function(token, goalId, description) {
    const goalDetailUrl = `${goalsListUrl}${goalId}/`;
    const data = { description };
    return axios.patch(goalDetailUrl, data, this.getOptions(token));
  },

  deleteGoal: function(token, goalId) {
    const goalDetailUrl = `${goalsListUrl}${goalId}/`;
    return axios.delete(goalDetailUrl, this.getOptions(token));
  },

  deleteMember: function(token, teamId, memberId) {
    const teamMemberDetailUrl = `${teamListUrl}${teamId}/members/${memberId}/`;
    return axios.delete(teamMemberDetailUrl, this.getOptions(token));
  },

  archiveGoalsDone: function(token, teamId) {
    const teamArchiveDonelUrl = `${teamListUrl}${teamId}/archive_done/`;
    return axios.delete(teamArchiveDonelUrl, this.getOptions(token));
  },

  getTeamMember: function(teamId, teamMemberId) {
    const teamMemberDetaillUrl = `${teamListUrl}${teamId}/members/${teamMemberId}/`;
    return axios.get(teamMemberDetaillUrl);
  },

  createUser: function(email, first_name, last_name, password) {
    return axios.post(userListUrl, {
      email, first_name, last_name, password
    })
  },

  callTeam: function(token, teamId) {
    const teamCalllUrl = `${teamListUrl}${teamId}/call/`;
    return axios.get(teamCalllUrl, this.getOptions(token));
  },

  resendMemberInvitation: function(token, teamId, teamMemberId) {
    const teamMemberResendlUrl = `${teamListUrl}${teamId}/members/${teamMemberId}/resend/`;
    return axios.post(teamMemberResendlUrl, {}, this.getOptions(token));
  }
}

export default StandupApiClient;