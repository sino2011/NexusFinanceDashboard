<script setup>
import { Bar } from "vue-chartjs";
import { Line } from "vue-chartjs";
import { Doughnut } from "vue-chartjs";
import { ref, onMounted } from "vue";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
} from "chart.js";
import axios from "axios";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
  BarElement,
  BarController,
  ArcElement,
  DoughnutController,
);

const isVisible = ref(false);
const progress = ref(44.4);
const saving_progress = ref(69.1);
const isMiddleRowIntersecting = ref(false);
const isTableRowIntersecting = ref(false);
const tableRowRef = ref(null);
const middleRowRef = ref(null);
const emergencyTarget = ref([]);

const API_BASE = import.meta.env.PROD
  ? "https://yassinafify.pythonanywhere.com"
  : "";

const financialMetrics = ref({
  savings_target: 0,
  base_savings: 0,
  current_savings: 0,
  emergency_fund: 0,
  savings_history: [],
  emergency_history: [],
  deep_dive: {
    months: ["July", "August", "September", "October", "November", "December"],
    fixed_costs: [2200, 2200, 2200, 2200, 2200, 2200],
    variable_costs: [750, 800, 1450, 1220, 920, 1720],
  },
});

// Secure headers helper
const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return { headers: { Authorization: token ? `Bearer ${token}` : "" } };
};

function toggleSiderbar() {
  isVisible.value = !isVisible.value;
}

const getData = async () => {
  try {
    // Attached auth header
    const response = await axios.get(`${API_BASE}/Reports`, getAuthHeaders());

    console.log("Flask payload received:", response.data);
    financialMetrics.value = response.data;

    MidlleRowGraph.value.datasets[0].data =
      response.data?.deep_dive?.fixed_costs ||
      financialMetrics.value.deep_dive.fixed_costs;

    MidlleRowGraph.value.datasets[1].data =
      response.data?.deep_dive?.variable_costs ||
      financialMetrics.value.deep_dive.variable_costs;

    MidlleRowGraph.value = { ...MidlleRowGraph.value };
  } catch (error) {
    console.error("La rbna m3ak baa", error);
  }
};

function setNumber(digitElement, value) {
  const height = 50;
  const offset = value * height;
  digitElement.style.transform = `translateY(-${offset}px)`;
}

function updateSavingsDisplay(value) {
  const savingsStr = String(value).padStart(6, "0");
  const digitsArray = savingsStr.split("").map(Number);
  for (let i = 1; i <= 6; i++) {
    const el = document.getElementById("dig-" + i);
    if (el) setNumber(el, digitsArray[i - 1]);
  }
}

function updateEmergencyDisplay(value) {
  const emergencyStr = String(value).padStart(5, "0");
  const emergencyDigits = emergencyStr.split("").map(Number);
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById("digit-" + i);
    if (el) setNumber(el, emergencyDigits[i - 1]);
  }
}

onMounted(async () => {
  await getData();

  const observerOptions = {
    threshold: [0.4, 0.2],
    rootMargin: "0px 0px -10% 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        if (
          entry.target === middleRowRef.value &&
          entry.intersectionRatio >= 0.5
        ) {
          isMiddleRowIntersecting.value = true;
          observer.unobserve(entry.target);
        }
        if (
          entry.target === tableRowRef.value &&
          entry.intersectionRatio >= 0.1
        ) {
          isTableRowIntersecting.value = true;
          observer.unobserve(entry.target);
        }
      }
    });
  }, observerOptions);

  if (middleRowRef.value) observer.observe(middleRowRef.value);
  if (tableRowRef.value) observer.observe(tableRowRef.value);

  setTimeout(() => {
    let totalEmergency = 0;
    updateEmergencyDisplay(totalEmergency);

    const emergencyHistory = financialMetrics.value.emergency_history || [];
    totalEmergency = emergencyHistory.reduce((sum, value) => sum + value, 0);

    setTimeout(() => {
      updateEmergencyDisplay(totalEmergency);
      financialMetrics.value.emergency_current = totalEmergency;
    }, 100);

    const baseSavings = financialMetrics.value.base_savings || 0;
    updateSavingsDisplay(baseSavings);

    const savingsHistory = financialMetrics.value.savings_history || [];
    const totalExtraSavings = savingsHistory.reduce(
      (sum, value) => sum + value,
      0,
    );
    const finalSavingsTotal = baseSavings + totalExtraSavings;

    setTimeout(() => {
      updateSavingsDisplay(finalSavingsTotal);
      financialMetrics.value.current_savings = finalSavingsTotal;
    }, 100);
  }, 1700);
});

const SavingsData = {
  labels: [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ],
  datasets: [
    {
      label: "Savings",
      data: [12, 17, 15, 24, 19, 14, 20, 21, 18, 16, 22, 26],
      borderColor: "#00C853",
      backgroundColor: "rgba(74, 222, 128, 0.1)",
      fill: true,
      tension: 0.4,
      pointRadius: 0,
      pointBackgroundColor: "#ffffff",
    },
  ],
};

const donutData = {
  labels: ["Food", "Rent", "Entertainment", "Others"],
  datasets: [
    {
      backgroundColor: ["#4ADE80", "#818CF8", "#FBBF24", "#F87171"],
      data: [40, 30, 20, 10],
      borderWidth: 0,
      hoverOffset: 10,
    },
  ],
};

const MidlleRowGraph = ref({
  labels: ["July", "August", "September", "October", "November", "December"],
  datasets: [
    {
      label: "Fixed Essential Costs",
      data: [2200, 2200, 2200, 2200, 2200, 2200],
      borderColor: "rgba(163, 163, 181, 0.35)",
      borderWidth: 2,
      borderDash: [6, 6],
      fill: false,
      pointRadius: 0,
      hoverRadius: 0,
    },
    {
      label: "Variable / Discretionary",
      data: [750, 800, 1450, 1220, 920, 1720],
      borderColor: "#818CF8",
      backgroundColor: "rgba(129, 140, 248, 0.1)",
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: "#ffffff",
      pointBorderColor: "#818CF8",
      pointHoverRadius: 6,
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  resizeDelay: 0,
  animation: { duration: 400 },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: "#1E1E2F",
      titleColor: "#ffffff",
      bodyColor: "#A3A3B5",
      borderColor: "rgba(255, 255, 255, 0.1)",
      borderWidth: 1,
      displayColors: true,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: "rgba(255, 255, 255, 0.05)" },
      ticks: {
        color: "rgba(255, 255, 255, 0.6)",
        callback: function (value) {
          return "$" + value;
        },
      },
    },
    x: {
      grid: { display: false },
      ticks: { color: "rgba(255, 255, 255, 0.6)" },
    },
  },
};

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: "70%",
  plugins: {
    legend: {
      display: true,
      position: "bottom",
      labels: { color: "#ffffff", padding: 20 },
    },
  },
};
</script>

<template>
  <component is="style">
    @import
    url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
    @import
    url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
  </component>

  <div class="app-layout">
    <!-- <div class="toggle-btn-container" :class="{ shifted: isVisible }">
          <i
          class="fa-solid fa-bars"
        id="icon"
        @click="toggleSiderbar"
        style="margin-left: 15px; margin-top: 20px"
        ></i>
    </div> -->
    <!-- <Transition name="slide">
        <div class="SideBar" id="SideBar" v-show="isVisible">
            <RouterLink to="/Home" class="a">Home</RouterLink>
            <RouterLink to="/Transactions" class="a">Transactions</RouterLink>
            <RouterLink to="/Reports" class="a">Reports</RouterLink>
            <RouterLink to="/Settings" class="a">Settings</RouterLink>
        </div>
    </Transition> -->
    <div class="content-view">
      <div class="navBar">
        <div class="navItems">
          <RouterLink to="/Home" class="navItem">Home</RouterLink>
          <RouterLink to="/Transactions" class="navItem"
            >Transactions</RouterLink
          >
          <RouterLink to="/Reports" id="current" class="navItem"
            >Reports</RouterLink
          >
          <RouterLink to="/Settings" class="navItem">Settings</RouterLink>
        </div>
      </div>
      <div class="mainContainer">
        <div class="titles">
          <h1>Why the numbers moved</h1>
          <h2>the way they did.</h2>
        </div>
        <div class="Cards" :class="{ shifted: isVisible }">
          <div class="Total">
            <h3>Emergency Fund</h3>
            <div class="counter-row">
              <span class="currency-symbol">$</span>
              <div v-for="i in 5" :key="i" class="counter">
                <div class="digit-slot">
                  <div class="digit-strip" :id="'digit-' + i">
                    <span>0</span><span>1</span><span>2</span><span>3</span
                    ><span>4</span><span>5</span><span>6</span><span>7</span
                    ><span>8</span><span>9</span>
                  </div>
                </div>
              </div>
            </div>
            <p class="goal">
              Of ${{ financialMetrics.emergency_target }} target
            </p>
            <div class="Pro-container">
              <div
                class="Pro"
                :style="{
                  width:
                    (financialMetrics.emergency_current /
                      (financialMetrics.emergency_target || 1)) *
                      100 +
                    '%',
                }"
              >
                <span
                  v-if="
                    (financialMetrics.emergency_current /
                      (financialMetrics.emergency_target || 1)) *
                      100 >
                    10
                  "
                ></span>
              </div>
            </div>
            <p class="Eme">+$265/mo</p>
          </div>
          <div class="Savings">
            <h3>Savings</h3>
            <div class="counter-row">
              <span class="currency-symbol">$</span>
              <div v-for="i in 6" :key="i" class="counter">
                <div class="digit-slot">
                  <div class="digit-strip" :id="'dig-' + i">
                    <span>0</span><span>1</span><span>2</span><span>3</span
                    ><span>4</span><span>5</span><span>6</span><span>7</span
                    ><span>8</span><span>9</span>
                  </div>
                </div>
              </div>
            </div>
            <p class="target">
              Of ${{ financialMetrics.savings_target }} Target
            </p>
            <div class="Pro-container">
              <div
                class="Pro"
                :style="{
                  width:
                    (financialMetrics.current_savings /
                      (financialMetrics.savings_target || 1)) *
                      100 +
                    '%',
                }"
              >
                <span v-if="saving_progress > 10"></span>
              </div>
            </div>
            <p class="save">+$325/mo</p>
          </div>
        </div>
        <div class="Core">
          <div class="left">
            <div class="middle-card" :class="{ shifted: isVisible }">
              <div class="middle-chart-wrapper">
                <Line :data="MidlleRowGraph" :options="chartOptions" />
              </div>
              <h2>Deep Dive</h2>
              <p>Spending over last 6 months analysis.</p>
            </div>
          </div>
        </div>
        <div class="grid-transition-zone">
          <div
            class="quotes"
            ref="tableRowRef"
            :class="{ 'animate-trigger': isTableRowIntersecting }"
          >
            <div class="Right" :class="{ shifted: isVisible }">
              <div class="firstRow">
                <div class="bar" :class="{ shifted: isVisible }">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    aria-hidden="true"
                    data-slot="icon"
                    width="16"
                    height="16"
                    class="text-[#A3A3B5]"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                    ></path>
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                    ></path>
                  </svg>
                  <h3>The progress bar is the product.</h3>
                  <p class="bord">
                    Seeing a bar move 2% triggers the same dopamine loop as
                    completing a task. Visible progress compresses perceived
                    effort.
                  </p>
                  <h2>3.4x</h2>
                  <p>higher completion with visible tracking</p>
                </div>
                <div class="Donut-card">
                  <div class="w-8" style="background: rgba(163, 163, 181, 0.1)">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke-width="1.5"
                      stroke="currentColor"
                      aria-hidden="true"
                      data-slot="icon"
                      width="16"
                      height="16"
                      class="text-[#A3A3B5]"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z"
                      ></path>
                    </svg>
                  </div>
                  <h3>Known expenses should never be suprises.</h3>
                  <p class="bord">
                    Car registration. Holiday gifts. Annual subscriptions.
                    Divide the total by 12 and automate monthly deposits into
                    named buckets. The bill arrives — the money is already
                    there.
                  </p>
                  <h2>94%</h2>
                  <p class="stress">
                    of financial stress is from predictable costs
                  </p>
                </div>
              </div>
              <div class="secRow">
                <div class="auto">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    aria-hidden="true"
                    data-slot="icon"
                    width="16"
                    height="16"
                    class="text-[#A3A3B5]"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"
                    ></path>
                  </svg>
                  <h3>Remove willpower from the equation.</h3>
                  <p class="bord">
                    Auto-transfers scheduled for payday morning means the
                    decision was made once. Every subsequent month costs zero
                    cognitive load.
                  </p>
                  <h2>0</h2>
                  <p>decisions after the first one</p>
                </div>
                <div class="savingsAcc">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    aria-hidden="true"
                    data-slot="icon"
                    width="16"
                    height="16"
                    class="text-[#00C853]"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.25 18 9 11.25l4.306 4.306a11.95 11.95 0 0 1 5.814-5.518l2.74-1.22m0 0-5.94-2.281m5.94 2.28-2.28 5.941"
                    ></path>
                  </svg>
                  <h3>Your savings account might be costing you.</h3>
                  <p class="bord">
                    Moving $10,000 from 0.01% APY to 4.8% APY generates $479 in
                    passive income annually. That's a flight, a month of
                    groceries, or an extra mortgage payment.
                  </p>
                  <h2>+$479</h2>
                  <p>annual passive income on $10k moved</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:global(body) {
  background-color: #0f172a; /* Matches your app-layout background */
  background-image:
    linear-gradient(rgba(163, 163, 181, 0.1) 1px, transparent 0),
    linear-gradient(90deg, rgba(163, 163, 181, 0.1) 1px, transparent 0);
  background-size: 48px 48px;
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}

@keyframes fallIn {
  from {
    opacity: 0;
    transform: translateY(-300px);
  }

  to {
    opacity: 1;
    transform: translateY(0px);
  }
}

@keyframes bottomIn {
  from {
    opacity: 0;
    transform: translatex(100px);
  }

  to {
    opacity: 1;
    transform: translatex(0px);
  }
}

@keyframes SideEnter {
  from {
    opacity: 0;
    transform: translateX(-600px);
  }

  to {
    opacity: 1;
    transform: translateX(0px);
  }
}

@keyframes mobileFadeUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.list-enter-from,
.list-appear-from {
  opacity: 0;
  transform: translateY(30px);
}

.list-enter-active,
.list-appear-active {
  transition: all 0.5s ease-out;
}

.list-enter-to,
.list-appear-to {
  opacity: 1;
  transform: translateY(0);
}

.fade-enter-active {
  transition: opacity 0.8s ease;
}

a:hover {
  color: #ffffff;
}

a {
  transition: all 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.6s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

h1 {
  font-weight: 1000;
  letter-spacing: -0.02em;
  color: #ffffff;
}

h2 {
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  color: #ffffff;
}

h3 {
  color: #ffffff;
  letter-spacing: -0.02em;
  font-weight: 900;
}

p {
  font-weight: 400;
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
}

svg {
  color: rgb(163, 163, 181);
  /* width: 50px;
        height: 50px; */
}

.a {
  margin: 20px;
  overflow: hidden;
  text-decoration: none;
  color: #818cf8;
  z-index: -1;
}

.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #0f172a; /* Dark background to match your glass theme */
  overflow: hidden; /* Prevents unwanted scrollbars during animation */
  font-family: "Plus Jakarta Sans", sans-serif;
  background-color: #0f172a; /* Matches your app-layout background */
  background-image:
    linear-gradient(rgba(163, 163, 181, 0.1) 1px, transparent 0),
    linear-gradient(90deg, rgba(163, 163, 181, 0.1) 1px, transparent 0);
  background-size: 48px 48px;
}

.toggle-btn-container {
  position: fixed;
  top: 25px;
  left: 25px;
  z-index: 100; /* Always on top */
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.6s ease-in-out;
  transition: all 0.3s ease;
}

.toggle-btn-container.shifted {
  transform: translateX(10px);
}

.navBar {
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0 0 16px 16px;
  padding: 10px;
  margin-bottom: -40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 1000;
}

.navItems {
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-direction: row;
}

#current {
  text-decoration: underline;
}

.navItems a {
  text-decoration: none;
  color: #818cf8;
}

.a {
  margin: 20px;
  overflow: hidden;
  text-decoration: none;
  color: #818cf8;
  z-index: -1;
}

.content-view {
  flex: 1;
  min-width: 0;

  display: flex;
  flex-direction: column;

  overflow-y: auto;
  overflow-x: hidden;

  transition: padding-left 0.87s ease;
}

.Cards {
  display: flex; /* Grid is much more reliable for sizing */
  gap: 20px;
  width: 100%;
  transition: all 0.7s ease;
}

.Cards.shifted {
  margin-left: 270px;
  width: calc(100% - 270px);
}
.middle-card.shifted {
  margin-left: 270px;
  width: calc(100% - 270px);
}
.Right.shifted {
  margin-left: 270px;
  width: calc(100% - 270px);
}

.w-8 {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 25px;
  border-radius: 16px;
  height: 30px;
}

.topSpending {
  display: flex;
  flex: 1;
  min-width: 0;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 35vh;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: SideEnter 2s ease-in-out forwards;
  opacity: 0;
  padding: 20px;
  position: relative;
}

.Savings {
  display: flex;
  flex: 1;
  min-width: 0;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  height: 35vh;
  padding: 20px;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: SideEnter 2s ease-in-out forwards;
  overflow: hidden;
}

.Total {
  display: flex;
  flex: 1;
  min-width: 0;
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  height: 35vh;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: SideEnter 2s ease-in-out forwards;
  opacity: 0;
  padding: 20px;
}

.Total h1 {
  color: #00c853;
}

.counter-row {
  display: flex;
  align-items: center;
  justify-content: center;
}

.currency-symbol {
  font-size: 2rem;
  font-weight: bold;
  margin-right: 5px;
  color: #00c853;
}

.digit-slot {
  height: 50px;
  width: 30px;
  overflow: hidden;
  border-bottom: 2px solid rgba(129, 140, 248, 0.3);
}

.digit-strip {
  display: flex;
  flex-direction: column;
  transition: transform 2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.digit-strip span {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;
  font-size: 2rem;
  font-family: "JetBrains Mono", monospace;
  font-weight: bold;
  color: #ffffff;
}

.Savings h1 {
  color: #00c853;
}

.Total h3 {
  font-family:
    DM Sans,
    sans-serif;
  font-weight: 600;
  font-size: 1.25rem;
  line-height: 1.5rem;
}

.Savings h3 {
  font-family:
    DM Sans,
    sans-serif;
  font-weight: 600;
  font-size: 1.25rem;
  line-height: 1.5rem;
}

.Savings p {
  font-size: x-small;
  font-weight: 500;
}

.Pro-container {
  width: 100%;
  background-color: rgb(42 42 69);
  border-radius: 50px;
  margin: 20px 0px;
  transition: all 3s ease;
}

.goal {
  font-size: x-small;
  font-weight: 500;
}

.Eme {
  font-size: x-small;
  font-weight: 650;
  margin-top: -2px;
}

.save {
  font-size: x-small;
  font-weight: 650;
  margin-top: -2px;
}

.titles h2 {
  -tw-text-opacity: 1;
  color: rgb(163 163 181);
  font-size: 3vw;
  margin-left: 35px;
  font-family:
    DM Sans,
    sans-serif;
}

.titles h1 {
  -tw-text-opacity: 1;
  color: #ffffff;
  font-weight: 700;
  line-height: 1.25;
  font-size: 5vw;
  margin-left: 30px;
  margin-bottom: -20px;
  font-family:
    DM Sans,
    sans-serif;
}

.titles p {
  color: rgb(163 163 181);
  font-size: 1.125rem;
  margin-left: 50px;
}

.Pro {
  height: 7px;
  background-color: #00c853;
  border-radius: inherit;
  transition: width 0.4s ease-in-out; /* Smooth movement */
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  color: #00c853;
}

.Total:hover,
.topSpending:hover,
.Savings:hover {
  transform: translateY(-15px);
  box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
}

/* 2. Fix the chart container sizing */
.chartContainer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px; /* Ensure the chart has a specific height */
  padding: 0 10px;
}

.mainContainer {
  width: 100%;
  max-width: 100%;
  /* padding: 20px; */
  display: flex;
  flex-direction: column;
  gap: 30px; /* Space between Row 1 and Row 2 */
  /* overflow: ; */
  min-width: 0;
  position: relative;
  transition: margin-left 0.6s ease;
}

.grid-transition-zone {
  background:
    linear-gradient(to bottom, #22223d 0%, rgba(34, 34, 61, 0) 100%),
    linear-gradient(rgba(26, 26, 46, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(26, 26, 46, 0.04) 1px, transparent 1px), #f4f5f7;
  background-size:
    100% 150px,
    48px 48px,
    48px 48px,
    100% 100%;
  background-repeat: no-repeat, repeat, repeat, no-repeat;
  background-position: top left;

  position: relative;
  /* z-index: 1; */

  /* Removed overflow breakout calculations causing the shifting */
  width: 100%;
  margin-top: 40px;
  margin-bottom: 0px;
  padding: 100px 20px 70px; /* Kept standard padding boundaries */
  box-sizing: border-box;
  min-height: calc(100vh - 400px);
}

/* Row 2 Container */
.Core {
  display: flex;
  width: 100%;
  gap: 20px;
  height: 55vh; /* Adjust height as needed */
}

/* The 60% side */
.left {
  flex: 0 0 100%;
  min-width: 0;
  display: flex;
}

.Right {
  flex: 1;
  min-width: 0;
  display: flex;
  transition: all 0.7s ease;
}

.middle-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  animation: SideEnter 2s ease forwards;
  transition:
    all 0.7s ease,
    box-shadow 0.3s ease;
}

.firstRow,
.secRow {
  display: flex;
  gap: 20px;
  width: 100%;
  /* align-items: stretch; This forces children to be the same height */
}

.auto,
.bar,
.Donut-card,
.savingsAcc {
  flex: 1;
  background: rgba(255, 255, 255, 1);
  border-radius: 16px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  min-height: 50vh;
  height: 70vh;
  min-width: 0;
  margin-top: 60px;
  position: relative;
  overflow: hidden;
  animation: bottomIn 2s ease forwards;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;

  /* Removed specific side-margin differentials (.auto vs .bar) */
  margin-left: 0;
  margin-right: 0;
  margin-bottom: 10px;
}

.Donut-card,
.bar {
  margin-bottom: 10px;
  margin-right: 10px;
}

.auto,
.savingsAcc {
  margin-bottom: 10px;
  margin-left: 10px;
}

.auto h3,
.bar h3,
.Donut-card h3,
.savingsAcc h3 {
  font-family:
    DM Sans,
    sans-serif;
  color: #1a1a2e;
  line-height: 1.25;
  font-weight: 600;
  font-size: 1.25rem;
}

.auto p,
.bar p,
.Donut-card p,
.savingsAcc p {
  font-family: Manrope, sans-serif;
  color: rgb(163, 163, 181);
  line-height: 1.625;
  font-size: 0.875rem;
}

.auto h2,
.bar h2,
.savingsAcc h2,
.Donut-card h2 {
  color: #1a1a2e;
  font-family:
    JetBrains Mono,
    monospace;
  font-weight: 700;
  font-size: 1.875rem;
  line-height: 2.25rem;
}

.Donut-card h3 {
  line-height: 1.25;
  font-weight: 600;
  font-size: 1.25rem;
}

.Donut-card h2 {
  line-height: 2.25;
  font-weight: 700;
  font-size: 1.875rem;
}

.stress {
  margin-top: -18px;
  font-size: 0.75rem;
  line-height: 1rem;
}

.bord {
  padding-bottom: 10%;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  line-height: 1.625;
  font-size: 0.875rem;
}

.middle-card:hover,
.Donut-card:hover,
.auto:hover,
.savingsAcc:hover,
.bar:hover {
  transform: translateY(-15px);
  box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
}

/* Ensure the chart has room to grow */
.middle-chart-wrapper {
  flex-grow: 1; /* Makes chart take up available space in card */
  width: 100%;
  min-height: 0; /* Important for Chart.js resizing */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 15px;
}

.quotes {
  opacity: 0;
  transition: opacity 0.5 ease;
}

.animate-trigger {
  animation: SideEnter 1.5s ease-out forwards;
}

@media (max-width: 1024px) {
  .app-layout {
    height: auto;
    overflow-y: auto;
  }

  .content-view {
    padding-left: 0;
  }

  .titles {
    margin: 10px;
  }

  .titles h1 {
    font-size: 8vw;
    margin-left: 15px;
  }

  .titles h2 {
    font-size: 6vw;
    margin-left: 18px;
  }

  .Cards {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 95%;
    gap: 12px;
    margin: 10px;
  }

  .Total,
  .Savings,
  .topSpending {
    width: min(100%, 520px);
    height: auto;
    min-height: 220px;
    padding: 16px;
  }

  .Core,
  .Right,
  .firstRow,
  .secRow {
    flex-direction: column;
    gap: 12px;
    height: auto;
    width: 100%;
  }

  .middle-card,
  .Donut-card,
  .auto,
  .bar,
  .savingsAcc {
    width: 95%;
    height: auto;
    min-height: auto;
    margin: 10px;
    padding: 24px;
    animation: none;
  }

  .middle-card.shifted,
  .Cards.shifted,
  .Right.shifted {
    margin-left: 0;
    width: 100%;
  }

  .SideBar {
    left: 0;
    top: 0;
    width: 340px;
    height: 100vh;
    border-radius: 0 16px 16px 0;
    background: rgba(15, 23, 42, 0.95);
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
  }

  .toggle-btn-container.shifted {
    transform: translateX(0px);
  }

  .grid-transition-zone {
    width: 100%;
    padding: 40px 15px;
  }

  .quotes.animate-trigger {
    animation: mobileFadeUp 1.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
  }

  .bord {
    padding-bottom: 15px;
  }
}

@media (max-width: 768px) {
  .app-layout {
    height: auto;
    min-height: 100vh;
    overflow: visible;
  }

  .content-view {
    overflow: visible;
  }

  .navItems {
    flex-wrap: wrap;
    gap: 8px;
  }

  .Cards {
    flex-direction: column;
    gap: 12px;
  }

  .Core {
    flex-direction: column;
    height: auto;
  }

  .left,
  .Right {
    flex: 1 1 100%;
  }

  .Total,
  .Savings,
  .topSpending {
    height: auto;
    min-height: auto;
    padding: 16px;
    width: 100%;
  }

  .chartContainer {
    display: none;
  }

  .middle-card,
  .Donut-card {
    height: auto;
    min-height: auto;
    padding: 20px;
    width: 100%;
    margin: 0;
  }

  .SideBar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    width: 80%;
    max-width: 300px;
    margin: 0;
    border-radius: 0 16px 16px 0;
  }

  .mainContainer {
    display: flex;
    justify-content: center;
    align-items: stretch;
    padding-top: 56px;
    padding-left: 0;
    padding-right: 0;
  }

  .titles h1,
  .titles h2,
  .titles p {
    margin-left: 0;
  }

  .counter-row {
    flex-wrap: wrap;
    gap: 4px;
  }

  .digit-slot {
    height: 42px;
    width: 22px;
  }

  .digit-strip span {
    height: 42px;
    font-size: 1.35rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  p {
    font-size: 0.85rem;
  }
}

@media (max-width: 1024px) {
  .Cards {
    flex-direction: column;
  }

  .Total,
  .Savings {
    width: 100%;
    height: auto;
  }

  .firstRow,
  .secRow {
    flex-direction: column;
  }

  .bar,
  .Donut-card,
  .auto,
  .savingsAcc {
    width: 100%;
    margin: 0;
  }

  .middle-chart-wrapper {
    height: 240px;
  }
}

@media (max-width: 480px) {
  .titles h1 {
    font-size: 1.45rem;
  }

  .titles h2 {
    font-size: 1.1rem;
  }

  .middle-chart-wrapper {
    height: 200px;
  }

  .Total,
  .Savings,
  .middle-card,
  .bar,
  .Donut-card,
  .auto,
  .savingsAcc {
    width: 95%;
    margin: 10px;
  }

  .firstRow,
  .secRow {
    gap: 12px;
  }
}
</style>
