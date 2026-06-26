<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, nextTick, computed } from "vue";
import { Bar } from "vue-chartjs";
import { Line } from "vue-chartjs";
import axios from "axios";
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
} from "chart.js";

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
);

const isLoadingHome = ref(true);
const isVisible = ref(false);
const middleRowRef = ref(null);
const tableRowRef = ref(null);
const isIntersecting = ref(false);
const isTableVisible = ref(false);
const Home = ref(0);
const progress = ref(100);
const calculationsData = ref({});
const homeMetrics = ref({
  total_savings: 0,
  monthly_contributed: 0,
  debt_contributions: 0,
});
const tables = ref([]);

// Helper function to dynamically add authorization headers
const getAuthHeaders = () => {
  let token = localStorage.getItem("token");
  if (!token) {
    console.warn("No token found in localStorage!");
    return {};
  }

  // Clean up token string if it accidentally has double quotes or manual "Bearer " wrapped around it
  token = token.replace(/^["']|["']$/g, "").trim();
  if (token.startsWith("Bearer ")) {
    token = token.slice(7).trim();
  }

  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
};

const formatCompletionDate = (dateString) => {
  if (!dateString || dateString === "---") return "---";
  const date = new Date(dateString);
  if (!isNaN(date.getTime())) {
    return date.toLocaleDateString("en-US", {
      month: "short",
      year: "numeric",
    });
  }
  return dateString;
};

const isProfileIncomplete = computed(() => {
  const data = calculationsData.value;
  return !data || !data.savings_target || data.savings_target === 0;
});

const getProjectedDate = (monthsToGoal) => {
  if (!monthsToGoal || isNaN(monthsToGoal)) return "---";
  const d = new Date();
  d.setMonth(d.getMonth() + monthsToGoal);
  return d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
};

const balancedProgress = computed(() => {
  const target = calculationsData.value.savings_target;
  const current = calculationsData.value.balance_36mo;
  if (!target || !current || target === 0) return 0;
  return Math.min(Math.round((current / target) * 100), 100);
});

const aggressiveProgress = computed(() => {
  const target = calculationsData.value.savings_target;
  const current = calculationsData.value.balance_36mo;
  if (!target || !current || target === 0) return 0;
  return Math.min(Math.round(((current * 1.2) / target) * 100), 100);
});

const conservativeProgress = computed(() => {
  const target = calculationsData.value.savings_target;
  const current = calculationsData.value.balance_36mo;
  if (!target || !current || target === 0) return 0;
  return Math.min(Math.round(((current * 0.8) / target) * 100), 100);
});

const getDigitsArray = (num, length) => {
  const str = Math.floor(num).toString().padStart(length, "0");
  return str.split("").map(Number);
};

const fetchHomeData = async () => {
  try {
    isLoadingHome.value = true;
    const response = await axios.get(
      "https://yassinafify.pythonanywhere.com/home",
      getAuthHeaders(),
    );

    if (response.data && response.data.profile) {
      calculationsData.value = response.data.profile;
    }

    // Direct data assignment from new backend keys
    homeMetrics.value = {
      total_savings: response.data.total_calculated_savings ?? 0,
      monthly_contributed: response.data.current_monthly ?? 0,
      debt_contributions: response.data.current_debt ?? 0,
    };

    const targetGoal = 10000;
    const calculationPercentage =
      (homeMetrics.value.debt_contributions / targetGoal) * 100;
    Home.value = Math.min(calculationPercentage, 100);

    const backendChartData = response.data.monthly_averages_chart || [];
    if (backendChartData.length > 0) {
      chartData2.value = {
        labels: [...chartData2.value.labels],
        datasets: [{ ...chartData2.value.datasets[0], data: backendChartData }],
      };
      const activeMonths = backendChartData.filter((val) => val !== 0);
      const totalSum = activeMonths.reduce((a, b) => a + b, 0);
      const finalAverage =
        activeMonths.length > 0 ? totalSum / activeMonths.length : 0;
      overallAverageLabel.value = `$${finalAverage.toFixed(2)}`;
    }

    await nextTick();
    setTimeout(() => {
      animateCounters();
    }, 1600);
  } catch (error) {
    console.error("Error fetching home data: ", error);
  } finally {
    isLoadingHome.value = false;
  }
};

const fetchSubscriptions = async () => {
  try {
    const response = await axios.get(
      "https://yassinafify.pythonanywhere.com/api/subscriptions",
      getAuthHeaders(),
    );

    // Log this directly to the console so you can inspect the exact key names returned by the DB
    console.log("Subscriptions raw response payload:", response.data);

    if (!Array.isArray(response.data)) {
      console.error("Expected array but received:", response.data);
      tables.value = [];
      return;
    }

    tables.value = response.data.map((item) => {
      // Safely access properties whether the DB column has an 's' or not
      const price =
        item.subscription_price !== undefined &&
        item.subscription_price !== null
          ? item.subscription_price
          : 0;

      const statusValue =
        item.subscriptions_status || item.subscription_status || "Pending";

      return {
        id: item.id,
        name: item.subscription_name || "Unknown Subscription",
        value: `${price}$`,
        status: statusValue,
      };
    });
  } catch (error) {
    console.error("Error connecting with backend subscription pipeline", error);
  }
};

const deleteSubscription = async (id) => {
  try {
    // Added Auth Headers
    const response = await axios.delete(
      `https://yassinafify.pythonanywhere.com/api/subscriptions/${id}`,
      getAuthHeaders(),
    );
    if (response.status === 200) {
      tables.value = tables.value.filter((tx) => tx.id !== id);
    }
  } catch (error) {
    console.error("Error deleting the subscription", error);
  }
};

const animateCounters = () => {
  const savingsValue = Number(homeMetrics.value.total_savings) || 0;
  const totalSavingsDigits = getDigitsArray(homeMetrics.value.total_savings, 6);
  totalSavingsDigits.forEach((digitValue, index) => {
    const el = document.getElementById(`dig-${index + 1}`);
    if (el) setNumber(el, digitValue);
  });

  const monthlyValue = Number(homeMetrics.value.monthly_contributed) || 0;
  const monthlyContDigits = getDigitsArray(monthlyValue, 4);
  monthlyContDigits.forEach((digitValue, index) => {
    const el = document.getElementById(`digi-${index + 1}`);
    if (el) {
      setNumber(el, digitValue);
    } else {
      console.error(`Missing DOM ID: "digi-${index + 1}" was not found.`);
    }
  });

  const debtValue = Number(homeMetrics.value.debt_contributions) || 0;
  const homeDebtDigits = getDigitsArray(debtValue, 4);
  homeDebtDigits.forEach((digitValue, index) => {
    const el = document.getElementById(`digit-${index + 1}`);
    if (el) {
      setNumber(el, digitValue);
    } else {
      console.error(`Missing DOM ID: "digit-${index + 1}" was not found.`);
    }
  });
};

onMounted(() => {
  fetchHomeData();
  fetchSubscriptions();

  const observerOptions = {
    threshold: 0.4,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        if (entry.target === middleRowRef.value) {
          isIntersecting.value = true;
          observer.unobserve(entry.target);
        }

        if (entry.target === tableRowRef.value) {
          isTableVisible.value = true;
          observer.unobserve(entry.target);
        }
      }
    });
  }, observerOptions);

  if (middleRowRef.value) observer.observe(middleRowRef.value);
  if (tableRowRef.value) observer.observe(tableRowRef.value);
});

const chartData = {
  labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
  datasets: [
    {
      label: "Spending",
      data: [380, 440, 500, 610],
      borderColor: "#818CF8",
      backgroundColor: "rgba(129, 140, 248, 0.2)",
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: "#ffffff",
    },
  ],
};

const chartData2 = ref({
  labels: [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ],
  datasets: [
    {
      label: "Net Flow Surplus",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      borderColor: "#818CF8",
      backgroundColor: "rgba(129, 140, 248, 0.2)",
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: "#ffffff",
    },
  ],
});

const overallAverageLabel = ref("0$");

const ChartData3 = {
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
      label: "Subscriptions",
      data: [4, 4, 5, 6, 5, 3, 7, 5, 2, 6, 2, 7, 6],
      backgroundColor: "#818CF8",
      borderRadius: 8,
      hoverBackgroundColor: "#ffffff",
    },
  ],
};

const MidlleRowGraph = {
  labels: ["July", "August", "September", "October", "November", "December"],
  datasets: [
    {
      label: "Spendings over last 6 months",
      data: [2950, 3000, 3650, 3420, 3120, 3920],
      borderColor: "#818CF8",
      backgroundColor: "rgba(129, 140, 248, 0.2)",
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: "#ffffff",
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: "rgba(255, 255, 255, 0.1)" },
      ticks: { color: "rgba(255, 255, 255, 0.7)" },
    },
    x: {
      grid: { display: false },
      ticks: { color: "rgba(255, 255, 255, 0.7)" },
    },
  },
};

function toggleSiderbar() {
  isVisible.value = !isVisible.value;
}

function setNumber(digitElement, value) {
  const height = 50;
  const offset = value * height;
  digitElement.style.transform = `translateY(-${offset}px)`;
}
</script>

<template>
  <link
    href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap"
    rel="stylesheet"
  />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Manrope:wght@200..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
    rel="stylesheet"
  />
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css"
    integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw=="
    crossorigin="anonymous"
    referrerpolicy="no-referrer"
  />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap"
    rel="stylesheet"
  />
  <!-- <div class="Side" id="side">
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
  <div class="main-container" :class="{ Shifted: isVisible }">
    <div class="navBar">
      <div class="navItems">
        <RouterLink to="/Home" id="current" class="navItem">Home</RouterLink>
        <RouterLink to="/Transactions" class="navItem">Transactions</RouterLink>
        <RouterLink to="/Reports" class="navItem">Reports</RouterLink>
        <RouterLink to="/Settings" class="navItem">Settings</RouterLink>
      </div>
    </div>
    <div class="titleContainer" :class="{ shifted: isVisible }">
      <h1 class="mainTitle">Watch your money</h1>
      <h2 class="subTitle">learn where to go.</h2>
      <p class="titleDisc">
        Three goals. One dashboard. Every dollar tagged, every milestone mapped
        against a timeline only you control.
      </p>
    </div>
    <div class="hero">
      <div class="Card1">
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
              d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
            ></path>
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
            ></path>
          </svg>
        </div>
        <h3>Small numbers, exponential outcomes.</h3>
        <p class="bor">
          Depositing $23 every weekday — the cost of one lunch — yields $6,240
          in twelve months. Not because $23 is large. Because it never stops.
        </p>
        <h2 class="colGreen">$8,395</h2>
        <p class="Mini">From $23/day over 12 Months.</p>
      </div>
      <div class="Card2">
        <div class="chart-wrapper">
          <Line
            v-if="
              !isLoadingHome &&
              chartData2.datasets[0].data.some((val) => val !== 0)
            "
            :data="chartData2"
            :options="chartOptions"
          />
          <div v-else-if="isLoadingHome" class="graph-placeholder">
            <i class="fa-solid fa-circle-notch fa-spin placeholder-icon"></i>
            <p>Loading your financial data...</p>
          </div>
          <div v-else class="graph-placeholder">
            <i class="fa-solid fa-chart-line placeholder-icon"></i>
            <p>Missing critical information</p>
            <span>Please fill the required information in settings</span>
          </div>
        </div>
        <h2>Monthly average</h2>
        <p>Your monthly average is {{ overallAverageLabel }}</p>
      </div>
      <div class="Card3">
        <h2 class="subject">Home Down Payment</h2>
        <div class="counter-row">
          <span class="currency-symbol">$</span>
          <div v-for="i in 4" :key="i" class="counter">
            <div class="digit-slot">
              <div class="digit-strip" :id="'digit-' + i">
                <span>0</span><span>1</span><span>2</span><span>3</span
                ><span>4</span><span>5</span><span>6</span><span>7</span
                ><span>8</span><span>9</span>
              </div>
            </div>
          </div>
        </div>
        <p class="target">Of $10,000 target</p>
        <div class="Pro-container">
          <div class="Pro" :style="{ width: Home + '%' }"></div>
        </div>
      </div>
    </div>
    <div class="horCardContainer">
      <div class="horCard">
        <div class="totSave">
          <h5>Total Saved</h5>
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
        </div>
        <div class="monthCont">
          <h5>Monthly Contributed</h5>
          <div class="counter-row">
            <span class="currency-symbol">$</span>
            <div v-for="i in 4" :key="i" class="counter">
              <div class="digit-slot">
                <div class="digit-strip" :id="'digi-' + i">
                  <span>0</span><span>1</span><span>2</span><span>3</span
                  ><span>4</span><span>5</span><span>6</span><span>7</span
                  ><span>8</span><span>9</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="grid-transition-zone">
      <div
        ref="middleRowRef"
        class="MiddleRow"
        :class="{ 'animate-trigger': isIntersecting }"
      >
        <div class="middle-card">
          <table class="plan">
            <thead>
              <tr>
                <th class="Met">Metric</th>
                <th>Aggressive</th>
                <th>Balanced</th>
                <th class="Con">Conservative</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="mon">Monthly Savings</td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.monthly_savings * 1.2 || 0,
                    ).toLocaleString(undefined, {
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    })
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.monthly_savings || 0,
                    ).toLocaleString(undefined, {
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    })
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.monthly_savings * 0.8 || 0,
                    ).toLocaleString(undefined, {
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    })
                  }}
                </td>
              </tr>
              <tr>
                <td class="mon">Savings Rate</td>
                <td id="plan">
                  {{ (calculationsData.savings_rate * 1.2 || 0).toFixed(1) }}%
                </td>
                <td id="plan">{{ calculationsData.savings_rate || 0 }}%</td>
                <td id="plan">
                  {{ (calculationsData.savings_rate * 0.8 || 0).toFixed(1) }}%
                </td>
              </tr>
              <tr>
                <td class="mon">Balance at 36mo</td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.balance_36mo * 1.2 || 0,
                    ).toLocaleString(undefined, {
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    })
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(calculationsData.balance_36mo || 0).toLocaleString(
                      undefined,
                      { minimumFractionDigits: 0, maximumFractionDigits: 0 },
                    )
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.balance_36mo * 0.8 || 0,
                    ).toLocaleString(undefined, {
                      minimumFractionDigits: 0,
                      maximumFractionDigits: 0,
                    })
                  }}
                </td>
              </tr>
              <tr>
                <td class="mon">Target Timeline</td>
                <td>
                  {{
                    calculationsData.time_to_goal
                      ? calculationsData.time_to_goal - 4
                      : 0
                  }}
                  Months
                </td>
                <td>{{ calculationsData.time_to_goal || 0 }} Months</td>
                <td>
                  {{
                    calculationsData.time_to_goal
                      ? calculationsData.time_to_goal + 12
                      : 0
                  }}
                  Months
                </td>
              </tr>
              <tr>
                <td class="mon">Completion Date</td>
                <td id="plan">
                  {{
                    getProjectedDate(
                      calculationsData.time_to_goal
                        ? calculationsData.time_to_goal - 4
                        : 0,
                    )
                  }}
                </td>
                <td id="plan">
                  {{ getProjectedDate(calculationsData.time_to_goal || 0) }}
                </td>
                <td id="plan">
                  {{
                    getProjectedDate(
                      calculationsData.time_to_goal
                        ? calculationsData.time_to_goal + 12
                        : 0,
                    )
                  }}
                </td>
              </tr>
              <tr>
                <td class="mon">Total Contributed</td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.total_contributed * 1.2 || 0,
                    ).toLocaleString()
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.total_contributed || 0,
                    ).toLocaleString()
                  }}
                </td>
                <td id="plan">
                  ${{
                    Number(
                      calculationsData.total_contributed * 0.8 || 0,
                    ).toLocaleString()
                  }}
                </td>
              </tr>
              <tr>
                <td class="mon">Time to Goal</td>
                <td id="plan">
                  {{ calculationsData.time_to_goal || 0 }} Months
                </td>
                <td id="plan">
                  {{ calculationsData.time_to_goal || 0 }} Months
                </td>
                <td id="plan">
                  {{ calculationsData.time_to_goal || 0 }} Months
                </td>
              </tr>
              <tr>
                <td class="mon">Progress at 36mo</td>
                <td>
                  <div class="Pro-container">
                    <div
                      class="Pro"
                      :style="{ width: aggressiveProgress + '%' }"
                    ></div>
                  </div>
                </td>
                <td>
                  <div class="Pro-container">
                    <div
                      class="Pro"
                      :style="{ width: balancedProgress + '%' }"
                    ></div>
                  </div>
                </td>
                <td>
                  <div class="Pro-container">
                    <div
                      class="Pro"
                      :style="{ width: conservativeProgress + '%' }"
                    ></div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="bottomRow" ref="tableRowRef">
        <Transition name="fade" mode="out-in">
          <table class="botTable" v-if="isTableVisible && tables.length > 0">
            <thead>
              <tr>
                <th>Number</th>
                <th>Subscriptions</th>
                <th>Value</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <TransitionGroup name="list" tag="tbody" appear>
              <tr
                v-for="(item, index) in tables"
                :key="item.id"
                :style="{ transitionDelay: `${index * 0.1}s` }"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.value }}</td>
                <td>{{ item.status }}</td>
                <td class="text-center">
                  <button
                    class="delete-btn"
                    @click="deleteSubscription(item.id)"
                    title="Delete Subscription"
                  >
                    <i class="fa-solid fa-trash-can"></i>
                  </button>
                </td>
              </tr>
            </TransitionGroup>
          </table>
          <div
            v-else-if="isTableVisible && tables.length === 0"
            class="table-placeholder"
          >
            <i class="fa-solid fa-wallet placeholder-icon"></i>
            <h4>Missing critical information</h4>
            <p>
              Please fill the required information in settings to track your
              subscriptions.
            </p>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  min-height: 100vh;
  background: #0f172a;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  background-attachment: fixed;
}
</style>

<style scoped>
@keyframes fallIn {
  from {
    opacity: 0;
    transform: translateY(-300px);
  }

  to {
    opacity: 1;
    transform: translateY(20px);
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

@keyframes SideEnterRight {
  from {
    opacity: 0;
    transform: translateX(600px);
  }

  to {
    opacity: 1;
    transform: translateX(0px);
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

.fade-enter-from {
  opacity: 0;
}

h2 {
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
  color: #ffffff;
}

p {
  font-weight: 400;
  font-size: 0.95rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.7);
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

.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  transition: all 0.1s ease;
  box-sizing: border-box;
  overflow-x: hidden;
}

.titleContainer {
  animation: SideEnter 1.9s ease-in-out;
  transition: all 0.7s ease-in-out;
}

.titleContainer.shifted {
  margin-left: 250px;
  width: calc(100% - 100px);
}

.main-container.Shifted {
  padding-left: 20px;
  max-width: 100%;
}

.main-container.Shifted .MiddleRow,
.main-container.Shifted .botTable,
.main-container.Shifted .horCard {
  max-width: 100%;
}

.mainTitle {
  font-family:
    DM Sans,
    sans-serif;
  font-size: 6vw;
  color: rgb(255, 255, 255);
  letter-spacing: -0.04em;
  line-height: 0.92;
  font-weight: 700;
  margin-bottom: -60px;
  margin-left: 30px;
}

.subTitle {
  color: rgba(163, 163, 181, 1);
  font-size: 6vw;
  font-family:
    DM Sans,
    sans-serif;
  letter-spacing: -0.04em;
  line-height: 0.92;
  font-weight: 700;
  margin-left: 30px;
}

.titleDisc {
  font-family: Manrope, sans-serif;
  color: rgb(163, 163, 181);
  line-height: 1.75rem;
  font-size: 1.125rem;
  margin-left: 30px;
}

.SideBar {
  position: fixed;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 17%;
  height: 97vh;
  margin-left: 10px;
  margin-top: 10px;
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  transition: all 1s ease-in-out;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 999;
  font-family: "Plus Jakarta Sans", sans-serif;
  color: #ffffff;
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

.a[data-v-817427b0]:hover {
  color: #ffffff;
  background: rgba(129, 140, 248, 0.1);
  text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
}

.hero {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 20px;
  font-family: "Plus Jakarta Sans", sans-serif;
  color: #ffffff;
  transition: all 0.7s ease-in-out;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 80px;
  padding: 0px 13px 0px 13px;
}

.main-container.Shifted .hero {
  transform: translateX(0);
  margin-left: 19%;
  width: 76vw;
}

.main-container.Shifted .horCard {
  transform: translateX(0);
  margin-left: 16%;
  width: 74vw;
}

.Card1 {
  display: flex;
  flex: 1;
  min-width: 0;
  justify-content: space-evenly;
  gap: 0px;
  align-items: flex-start;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 50vh;
  overflow: hidden;
  /* margin-top: 5px; */
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: SideEnter 2s ease-in-out forwards;
  opacity: 0;
  padding: 20px;
}

.Card1 h3 {
  font-family:
    DM Sans,
    sans-serif;
  color: rgb(255, 255, 255);
  line-height: 1.25;
  font-weight: 600;
  font-size: 1.25rem;
}

.Card1 p {
  font-family: Manrope, sans-serif;
  margin-top: -30px;
}

.colGreen {
  color: #00c853;
  font-family:
    JetBrains Mono,
    monospace;
  font-weight: 700;
  font-size: 1.875rem;
  line-height: 2.25rem;
  padding: 0 0 20px 0;
}

.bor {
  border-bottom: 1px solid rgba(163, 163, 181, 0.1);
  padding-bottom: 12%;
  line-height: 1.625;
  font-family: Manrope, sans-serif;
}

.Mini {
  font-size: 0.75rem;
  line-height: 1rem;
}

.Card2 {
  display: flex;
  flex: 1;
  min-width: 0;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 50vh;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: fallIn 2s ease-in-out forwards;
  opacity: 0;
  padding: 20px;
  margin-bottom: 41px;
}

.Card3 {
  display: flex;
  flex: 1;
  min-width: 0;
  align-items: flex-start;
  flex-direction: column;
  justify-content: center;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 50vh;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(20px);
  animation: SideEnterRight 2s ease-in-out forwards;
  opacity: 0;
  padding: 20px;
  gap: 5vh;
}

.Card1:hover,
.Card2:hover,
.Card3:hover {
  transform: translateY(-15px);
  box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
}

.Card1 img,
.Card2 img,
.Card3 img {
  height: 35vh;
  width: 80%;
}

.w-8 {
  border-radius: 16px;
  width: 25px;
  height: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.grid-transition-zone {
  background:
    linear-gradient(
      to bottom,
      #111726 0%,
      rgba(30, 41, 59, 0.4) 30%,
      rgba(244, 245, 247, 0) 100%
    ),
    linear-gradient(rgba(15, 23, 42, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(15, 23, 42, 0.06) 1px, transparent 1px), #f4f5f7;

  background-size:
    100% 180px,
    48px 48px,
    48px 48px,
    100% 100%;

  background-position:
    top left,
    top left,
    top left,
    top left;

  background-repeat: no-repeat, repeat, repeat, no-repeat;
  position: relative;
  z-index: 1;
  width: 100vw;
  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;

  margin-top: 50px;
  margin-bottom: 0px;
  padding: 100px 40px 80px 40px;
  box-sizing: border-box;
  min-height: calc(100vh - 400px);
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

.Pro-container {
  display: flex;
  align-items: flex-start;
  width: 100%;
  background-color: rgb(42 42 69);
  border-radius: 50px;
  margin: 20px 0px;
}

.Pro {
  height: 7px;
  background-color: #00c853;
  border-radius: inherit;
  transition: width 0.4s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  color: #00c853;
  transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.chart-wrapper {
  width: 100%;
  height: 250px;
  margin-bottom: 20px;
  position: relative;
}

/* Graph Placeholder Styles */
/* .chart-wrapper {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    } */

.graph-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  /* background: rgba(255, 255, 255, 0.02); */
  /* border: 1px dashed rgba(255, 255, 255, 0.1); */
  border-radius: 8px;
  /* padding: 20px; */
}

/* Table Placeholder Styles */
.table-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-top: 10px;
}

/* Typography & Icon styling for placeholders */
.placeholder-icon {
  font-size: 1.8rem;
  color: #818cf8; /* Accent purple */
  margin-bottom: 12px;
  opacity: 0.8;
}

.graph-placeholder p,
.table-placeholder h4 {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: #a3a3b5;
  margin: 0 0 4px 0;
}

.graph-placeholder span,
.table-placeholder p {
  font-family: "Plus Jakarta Sans", sans-serif;
  font-size: 0.8rem;
  color: #a3a3b5; /* Subtitle muted gray */
  margin: 0;
}

.Side {
  position: fixed;
  top: 20px;
  left: 15px;
  z-index: 1000;
  cursor: pointer;
  color: #ffffff;
  font-size: 1.5rem;
}

.horCardContainer {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  margin-bottom: 50px;
  animation: SideEnter 2s ease-in-out forwards;
  transition: all 0.7s ease-in-out;
  width: 100%;
  box-sizing: border-box;
  z-index: 100;
}

.horCard {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-left: 12px;
  margin-right: 12px;
  animation: SideEnter 2s ease-in-out forwards;
  transition: all 0.7s ease-in-out;
}

.totSave {
  font-family:
    JetBrains Mono,
    monospace;
  color: rgb(163, 163, 181);
  margin-right: 20px;
  margin-left: 20px;
}

.monthCont {
  font-family:
    JetBrains Mono,
    monospace;
  color: rgb(163, 163, 181);
  margin-right: 20px;
  margin-left: 3px;
}

.saveH2 {
  color: #00c853;
}

.contH2 {
  color: #00c853;
}

.MiddleRow {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
  opacity: 0;
  transform: translateX(-50px);
  transition:
    opacity 0.6s ease-in-out,
    transform 0.6s ease-in-out,
    max-width 1s ease-in-out,
    width 1s ease-in-out;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
}

.animate-trigger {
  opacity: 1;
  transform: translateX(0);
}

.middle-chart-wrapper {
  height: 400px;
  width: 100%;
  overflow: hidden;
}

.bottomRow {
  display: flex;
  justify-content: center;
  padding: 20px;
  margin-top: 30px;
  width: 100%;
  box-sizing: border-box;
  min-height: 400px;
  transition: width 0.1s ease-in-out;
}

table.plan {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  transition:
    max-width 2s ease-in-out,
    width 2s ease-in-out;
}

.botTable {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  transition:
    max-width 0.1s ease-in-out,
    width 0.1s ease-in-out;
}

.botTable tr {
  transition:
    transform 0.1s cubic-bezier(0.25, 1, 0.5, 1),
    background-color 0.1s ease-in-out;
  will-change: transform;
}

.botTable tr:hover {
  background: rgba(26, 26, 46, 0.02);
  transform: scale(1.006);
  cursor: pointer;
}

.bottom-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 100vh;
  transition: padding 0.1s ease-in-out;
  padding: 20px;
  box-sizing: border-box;
  overflow-x: hidden;
}

.main-container.Shifted .MiddleRow {
  max-width: 1000px;
  width: 65%;
}

.main-container.Shifted .botTable {
  max-width: 1000px;
  width: 67%;
}

.subject {
  font-family:
    DM Sans,
    sans-serif;
  font-weight: 600;
  font-size: 1rem;
  font-size: 1.5rem;
}

.money {
  font-size: 3vw;
  color: #f4f5f7;
  font-family:
    JetBrains Mono,
    monospace;
  font-weight: 700;
  color: #00c853;
}

.target {
  font-family:
    JetBrains Mono,
    monospace;
  font-size: 0.75rem;
  line-height: 1rem;
}

table.plan {
  max-width: 1200px;
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  font-family: "Plus Jakarta Sans", sans-serif;
  background: transparent;
}

table.plan th {
  background-color: rgba(244, 245, 247, 0.95);
  border-right: 1px solid rgba(26, 26, 46, 0.08);
  color: #a3a3ae;
  text-align: left;
  padding: 16px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

table.plan td {
  padding: 16px;
  background: rgba(255, 255, 255, 1);
  border-bottom: 1px solid rgba(26, 26, 46, 0.08);
  font-size: 0.95rem;
  transition: all 0.3s ease;
  color: #1a1a2e;
  border-right: 1px solid rgba(26, 26, 46, 0.08);
}

table.plan tr:last-child td:first-child {
  border-bottom-left-radius: 16px;
}
table.plan tr:last-child td:last-child {
  border-bottom-right-radius: 16px;
}

.botTable {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  color: #ffffff;
  font-family: "Plus Jakarta Sans", sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
  animation: 1s ease-in-out;
  transition: 1s ease-in-out;
}

.botTable th {
  background: rgba(244, 245, 247, 0.95);
  color: #a3a3ae;
  text-align: left;
  padding: 16px;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  border-left: 1px solid rgba(26, 26, 46, 0.08);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.botTable td {
  padding: 16px;
  background-color: rgba(255, 255, 255, 1);
  color: #1a1a2e;
  border-bottom: 1px solid rgba(26, 26, 46, 0.08);
  border-right: 1px solid rgba(26, 26, 46, 0.08);
  font-size: 0.95rem;
  animation: 1s ease-in-out;
  transition: 1s ease-in-out;
}

.botTable tr:last-child td:first-child {
  border-bottom-left-radius: 16px;
}
.botTable tr:last-child td:last-child {
  border-bottom-right-radius: 16px;
}

.botTable tr {
  transition:
    transform 0.3s cubic-bezier(0.25, 1, 0.5, 1),
    background-color 0.3s ease;
  will-change: transform;
}

.botTable tr:hover {
  background: rgba(26, 26, 46, 0.02);
  transform: scale(1.012);
  cursor: pointer;
}

.botTable td {
  transition: background-color 0.3s ease;
}

.text-center {
  text-align: center;
}

.botTable .delete-btn {
  background: transparent;
  border: none;
  color: #ff4d4d;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.botTable .delete-btn:hover {
  background: rgba(255, 77, 77, 0.15);
  color: #ff6666;
  transform: scale(1.05);
}

.Con .Met {
  border-radius: 16px;
}

.mon {
  color: rgb(163, 163, 181, 1.2);
}

#plan {
  /* color: #ffffff; */
  font-size: 0.95rem;
}

#spe {
  color: #00c853;
}

.Card1 {
  animation-delay: 0.1;
}
.Card2 {
  animation-delay: 0.1;
}
.Card3 {
  animation-delay: 0.1;
}
.animate-trigger {
  animation: SideEnter 1.5s ease-out forwards;
}

@media (max-width: 1024px) {
  .navBar {
    margin-top: -70px;
    margin-bottom: 20px;
  }

  .navItems {
    flex-wrap: wrap;
    gap: 8px;
  }

  .hero {
    flex-direction: column;
    margin-bottom: 40px;
    padding: 0 15px;
  }

  .Card1,
  .Card2,
  .Card3 {
    width: 100%;
    min-height: auto;
    height: auto;
  }

  .horCardContainer {
    padding: 0 15px;
    box-sizing: border-box;
  }

  .horCard {
    flex-direction: column;
    gap: 16px;
    padding: 20px 15px;
    margin-left: 0;
    margin-right: 0;
  }

  .MiddleRow,
  .bottomRow {
    width: 100%;
    max-width: 100%;
  }

  .chart-wrapper,
  .middle-chart-wrapper {
    height: 240px;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .main-container {
    overflow-x: hidden;
    padding-top: 70px;
  }

  .titleContainer {
    margin-bottom: 16px;
    width: 95%;
    margin: 10px;
  }

  .mainTitle {
    font-size: 2.2rem;
    margin-left: 15px;
    margin-bottom: 8px;
  }

  .subTitle {
    font-size: 1.7rem;
    margin-left: 15px;
    line-height: 1.1;
  }

  .titleDisc {
    font-size: 0.95rem;
    margin-left: 15px;
    padding-right: 15px;
  }

  .titleContainer.shifted,
  .main-container.Shifted .hero,
  .main-container.Shifted .horCard,
  .main-container.Shifted .MiddleRow,
  .main-container.Shifted .botTable {
    margin-left: 0;
    width: 100%;
    transform: none;
  }

  .hero {
    flex-direction: column;
    margin-bottom: 32px;
    padding: 0 12px;
    width: 93%;
    margin: 16px;
  }

  .horCardContainer {
    padding: 0 12px;
  }

  .horCard {
    flex-direction: column;
    gap: 16px;
    padding: 20px 12px;
    margin-left: 0;
    margin-right: 0;
  }

  .totSave,
  .monthCont {
    margin: 0;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .grid-transition-zone {
    width: 100%;
    max-width: 100%;
    left: 0;
    right: 0;
    margin-left: 0;
    margin-right: 0;
    padding: 48px 12px 32px;
    box-sizing: border-box;
    overflow-x: hidden;
  }

  .MiddleRow {
    max-width: 100%;
    width: 100%;
    transform: none;
    overflow-x: auto;
  }

  .bottomRow {
    padding: 0;
    overflow-x: auto;
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  .plan,
  .botTable {
    min-width: 0;
    width: 100%;
  }

  .SideBar {
    width: 75%;
    height: 100vh;
    margin: 0;
    border-radius: 0 16px 16px 0;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
  }

  .main-container {
    padding-top: 70px;
  }

  .main-container.Shifted {
    padding-left: 0;
    opacity: 1;
    filter: none;
    pointer-events: auto;
  }

  .titleContainer {
    margin-bottom: 16px;
  }

  .counter-row {
    margin-bottom: 15px;
    flex-wrap: wrap;
    justify-content: center;
    gap: 6px;
  }

  .grid-transition-zone p,
  .grid-transition-zone span {
    display: block;
    margin-top: 10px;
    line-height: 1.4;
  }

  .Card1,
  .Card2,
  .Card3 {
    width: 100%;
    height: auto;
  }

  .Card1 p {
    padding-top: 12px;
  }

  .chart-wrapper,
  .middle-chart-wrapper {
    height: 220px;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .navItems {
    justify-content: space-around;
  }

  .mainTitle {
    font-size: 1.7rem;
    margin-left: 0;
    margin-bottom: 6px;
    line-height: 1.05;
  }

  .subTitle {
    font-size: 1.25rem;
    margin-left: 0;
    line-height: 1.1;
  }

  .titleDisc {
    font-size: 0.9rem;
    margin-left: 0;
    padding-right: 0;
    line-height: 1.5;
  }

  .hero,
  .horCardContainer {
    padding: 0 8px;
  }

  .Card1,
  .Card2,
  .Card3 {
    padding: 16px;
    min-height: auto;
    height: auto;
  }

  .grid-transition-zone {
    padding: 40px 10px 24px;
  }

  .MiddleRow,
  .bottomRow {
    padding: 0 8px;
  }

  .botTable th,
  .botTable td {
    padding: 10px 8px;
    font-size: 0.8rem;
    overflow-wrap: anywhere;
    word-break: break-word;
  }
}
</style>
