import { createRouter, createWebHistory } from "vue-router";
import MainFrame from "../components/MainFrame.vue";
import HomePage from "../views/HomePage.vue";
import AboutPage from "../views/AboutPage.vue";

const routes = [
  {
    path: "/",
    component: MainFrame,
    children: [
      { path: "", name: "Home", component: HomePage },
      { path: "about", name: "About", component: AboutPage },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
