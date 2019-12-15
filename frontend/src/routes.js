import Home from './pages/Home.vue';
import Team from './pages/Team.vue';
import TeamSettings from './pages/TeamSettings.vue';
import Login from './pages/Login.vue';
import TeamMemberRegistration from './pages/TeamMemberRegistration.vue';

import store from './store.js';


const isAuthenticated = () => {
  if(!localStorage.authenticatedUser) { return false; }
  const user = JSON.parse(localStorage.authenticatedUser);
  return user.token !== null;
}


const ifAuthenticated = (to, from, next) => {
  if (isAuthenticated()) {
    next()
    return
  }
  next('/login')
}

const ifNotAuthenticated = (to, from, next) => {
  if (!isAuthenticated()) {
    next()
    return
  }
  next('/')
}


const routes = [
  {
    path: '/',
    component: Home,
    name: 'home',
    beforeEnter: ifAuthenticated
  },
  {
    path: '/login',
    component: Login,
    name: 'login',
    beforeEnter: ifNotAuthenticated
  },
  {
    path: '/:teamId',
    component: Team,
    name: 'team'
  },
  {
    path: '/:teamId/settings',
    component: TeamSettings,
    name: 'teamSettings',
    beforeEnter: ifAuthenticated
  },
  {
    path: '/:teamId/:teamMemberId/signup/',
    component: TeamMemberRegistration,
    name: 'TeamMemberRegistration'
  },
];

export default routes;