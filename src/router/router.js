import Home from "@/views/TopRow.vue"; // Import your components
import Transactions from "../views/Transactions.vue"
import Settings from "@/views/Settings.vue";
import Reports from "@/views/Reports.vue";
import { createRouter, createWebHashHistory } from 'vue-router'

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
  history: createWebHashHistory('/NexusFinanceDashboard/'),
  routes,
});

export default router;
