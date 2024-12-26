import { createRouter, createWebHistory } from 'vue-router';
import App from '../App.vue'
import MainFrame from '../views/MainFrame.vue';
import AdminApp from '../views/AdminApp.vue';
import StudentApp from '../views/StudentApp.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: MainFrame,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminApp,
  },
  {
    path: '/student',
    name: 'Student',
    component: StudentApp,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path);
  console.log('Matched Components:', to.matched);
  next();
});



export default router;
