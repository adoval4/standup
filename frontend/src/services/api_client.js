import axios from 'axios';

const baseUrl = "//localhost:8000";
const apiBaseUrl = `${baseUrl}/api/v1`;
const teamListUrl = `${apiBaseUrl}/teams/`;
const goalsListUrl = `${apiBaseUrl}/goals/`;

const StandupApiClient = {

  auth: function(email, password) {
    const authUrl = `${baseUrl}/api-token-auth/`;
    return axios.post(authUrl, {username: email, password: password})
  },

  getOptions: function(token) {
    return { headers: { 'Authorization': `Token ${token}` } };
  },

  getTeams: function(token) {
    return axios.get(teamListUrl, this.getOptions(token));
  },

  retrieveTeam: function(token, teamId) {
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

  updateGoalStatus: function(token, goalId, status) {
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
}

export default StandupApiClient;