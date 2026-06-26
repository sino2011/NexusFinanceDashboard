import { createRouter, createWebHashHistory } from "vue-router";
import Transactions from "../views/Transactions.vue";
import Settings from "@/views/Settings.vue";
import Reports from "@/views/Reports.vue";
import Signup from "@/views/Signup.vue";
import TopRow from "@/views/TopRow.vue";
import Login from "@/views/Login.vue";

const routes = [
  {
    path: "/",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/Home",
    name: "Home",
    component: TopRow,
    meta: { requiresAccount: true },
  },
  {
    path: "/Transactions",
    name: "transactions",
    component: Transactions,
    meta: { requiresAccount: true },
  },
  {
    path: "/Reports",
    name: "Reports",
    component: Reports,
    meta: { requiresAccount: true },
  },
  {
    path: "/Settings",
    name: "Settings",
    component: Settings,
    meta: { requiresAccount: true },
  },
];

const router = createRouter({
  history: createWebHashHistory("/NexusFinanceDashboard/"),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      // return savedPosition
    } else {
      return { top: -10, left: 0 };
    }
  },
});

router.beforeEach((to, from, next) => {
  const hasToken = Boolean(localStorage.getItem("token"));

  if (to.meta.requiresAccount && !hasToken) {
    next({ name: "Login" });
  } else if ((to.name === "Login" || to.name === "Signup") && hasToken) {
    next({ name: "Home" });
  } else {
    next();
  }
});

export default router;
