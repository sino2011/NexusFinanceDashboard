import { createWebHistory, createRouter } from "vue-router";
import Home from "@/views/TopRow.vue"; // Import your components
import Transactions from "../views/Transactions.vue"
import Settings from "@/views/Settings.vue";
import Reports from "@/views/Reports.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/Transactions",
    name: "transactions",
    component: Transactions,
  },
  {
    path: "/Reports",
    name: "Reports",
    component: Reports,
  },
  {
    path: "/Settings",
    name: "Settings",
    component: Settings,
  },
];

const router = createRouter({
  history: createWebHistory(), // Use HTML5 history mode (recommended)
  routes,
});

export default router;
