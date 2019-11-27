import axios from 'axios';

const StandupApiClient = {

  baseUrl: "//localhost:8000",
  auth: function(email, password) {
    const authUrl = `${this.baseUrl}/api-token-auth/`;
    return axios.post(authUrl, {username: email, password: password})
  }
}

export default StandupApiClient;