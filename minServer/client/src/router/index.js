import Vue from 'vue';
import Router from 'vue-router';
import Hosts from '../components/Hosts.vue';
import Ping from '../components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Hosts',
      component: Hosts,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
