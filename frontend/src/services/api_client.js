import axios from 'axios';

const baseUrl = "//localhost:8000";
const apiBaseUrl = `${baseUrl}/api/v1`;
const teamListUrl = `${apiBaseUrl}/teams/`;

const StandupApiClient = {

  auth: function(email, password) {
    const authUrl = `${baseUrl}/api-token-auth/`;
    return axios.post(authUrl, {username: email, password: password})
  },

  getTeams: function(token) {
    const headers = { 'Authorization': `Token ${token}` };
    return axios.get(teamListUrl, { headers });
  },

  retrieveTeam: function(token, teamId) {
    const teamDetailUrl = `${teamListUrl}${teamId}/`;
    const headers = { 'Authorization': `Token ${token}` };
    return axios.get(teamDetailUrl, { headers });
  },

  createTeam: function(token, newTeamName) {
    const headers = { 'Authorization': `Token ${token}` };
    return axios.post(teamListUrl, { name: newTeamName }, { headers });
  }

}

export default StandupApiClient;