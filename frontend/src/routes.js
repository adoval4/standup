import Home from './pages/Home.vue';
import Team from './pages/Team.vue';
import TeamSettings from './pages/TeamSettings.vue';
import Login from './pages/Login.vue';

const routes = [
  {
    path: '/',
    component: Home,
    name: 'home'
  },
  {
    path: '/login',
    component: Login,
    name: 'login'
  },
  {
    path: '/:teamId',
    component: Team,
    name: 'team'
  },
  {
    path: '/:teamId/settings',
    component: TeamSettings,
    name: 'teamSettings'
  }
];

export default routes;