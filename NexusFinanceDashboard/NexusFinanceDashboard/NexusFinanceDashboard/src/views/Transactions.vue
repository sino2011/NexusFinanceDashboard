<script setup>
import { ref } from "vue";
import axios from "axios";
import { onMounted } from "vue";

const isVisible = ref(false);
const transactions = ref([]);

// Secure headers helper
const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return { headers: { Authorization: token ? `Bearer ${token}` : "" } };
};

const getData = async () => {
  try {
    // Attached auth header
    const response = await axios.get(
      "https://yassinafify.pythonanywhere.com/Transactions",
      getAuthHeaders(),
    );

    transactions.value = response.data.map((tx, index) => {
      const rawDate = new Date(tx.transaction_date);
      const formattedDate = rawDate.toLocaleDateString("en-US", {
        weekday: "short",
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
      return {
        id: tx.id,
        name: tx.transaction_name,
        amount: parseFloat(tx.transaction_value) || 0,
        date: formattedDate,
        category: "General",
        icon: "fa-wallet",
        type: "expense",
      };
    });
  } catch (error) {
    console.error("Error fetching data", error);
  }
};

const deleteTransaction = async (id) => {
  try {
    // Attached auth header
    const response = await axios.delete(
      `https://yassinafify.pythonanywhere.com/Transactions/${id}`,
      getAuthHeaders(),
    );
    if (response.status === 200) {
      transactions.value = transactions.value.filter((tx) => tx.id !== id);
    }
  } catch (error) {
    console.error("Error deleting transaction:", error);
    alert("Failed to delete transaction.");
  }
};

function toggleSiderbar() {
  isVisible.value = !isVisible.value;
}

onMounted(() => {
  getData();
});
</script>

<template>
  <component is="style">
    @import
    url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
    @import
    url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
  </component>

  <!-- <div class="Side" id="side">
    <i
      class="fa-solid fa-bars"
      id="icon"
      @click="toggleSiderbar"
      style="margin-left: 15px; margin-top: 20px"
    ></i>
  </div>
  <Transition name="slide">
    <div class="SideBar" id="SideBar" v-show="isVisible">
      <RouterLink to="/Home" class="a">Home</RouterLink>
      <RouterLink to="/Transactions" class="a">Transactions</RouterLink>
      <RouterLink to="/Reports" class="a">Reports</RouterLink>
      <RouterLink to="/Settings" class="a">Settings</RouterLink>
    </div>
  </Transition> -->

  <div class="navBar">
    <div class="navItems">
      <RouterLink to="/Home" class="navItem">Home</RouterLink>
      <RouterLink to="/Transactions" id="current" class="navItem"
        >Transactions</RouterLink
      >
      <RouterLink to="/Reports" class="navItem">Reports</RouterLink>
      <RouterLink to="/Settings" class="navItem">Settings</RouterLink>
    </div>
  </div>
  <div class="main-container" :class="{ Shifted: isVisible }">
    <div class="page-header">
      <h1>Transactions</h1>
      <p>Your recent activity and spending history</p>
    </div>
    <div class="transaction-feed">
      <div v-for="tx in transactions" :key="tx.id" class="tx-card">
        <div class="tx-icon-wrapper" :class="tx.type">
          <i :class="['fa-solid', tx.icon]"></i>
        </div>
        <div class="tx-info">
          <span class="merchant-name">{{ tx.name }}</span>
          <span class="category-tag">{{ tx.category }}</span>
        </div>
        <div class="tx-side-info">
          <span class="amount" :class="tx.type">
            {{ tx.type === "expense" ? "-" : "+" }}${{ tx.amount.toFixed(2) }}
          </span>
          <span class="date">{{ tx.date }}</span>
        </div>

        <div class="tx-actions">
          <button
            class="delete-btn"
            @click="deleteTransaction(tx.id)"
            title="Delete Transaction"
          >
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
body {
  margin: 0;
  background: #0f172a;
  min-height: 100vh;
  font-family: "Plus Jakarta Sans", sans-serif;
}
</style>

<style scoped>
/* @keyframes SideEnter {
        from {
            opacity: 0;
            transform: translateX(-600px);
        }

        to {
            opacity: 1;
            transform: translateX(0px);
        }
    } */

@keyframes DownEnter {
  from {
    opacity: 0;
    transform: translateY(100px);
  }

  to {
    opacity: 1;
    transform: translateY(0px);
  }
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

.main-container {
  transition: all 0.5s ease-in-out;
  padding: 60px 20px;
  max-width: 800px; /* Keeps the list from getting too wide on desktop */
  margin: 0 auto;
}

.main-container.Shifted {
  padding-left: 20%;
}

.page-header {
  margin-bottom: 30px;
  color: white;
}

.transaction-feed {
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: DownEnter 2s ease-in-out forwards;
  z-index: 1000;
}

/* The Row Card */
.tx-card {
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.025);
  box-shadow: 0 4px 30px rgb(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 16px;
  border-radius: 16px;
  transition: transform 0.2s;
  cursor: pointer;
}

.tx-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: scale(1.01);
}

/* Icon Styling */
.tx-icon-wrapper {
  width: 45px;
  height: 45px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.tx-icon-wrapper.expense {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}
.tx-icon-wrapper.income {
  background: rgba(74, 222, 128, 0.2);
  color: #4ade80;
}

/* Text Sections */
.tx-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 16px;
}

.merchant-name {
  font-weight: 600;
  color: white;
  font-size: 1.1rem;
}

.category-tag {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.5);
}

.tx-side-info {
  text-align: right;
  display: flex;
  flex-direction: column;
}

.tx-card {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Ensures side info elements push content wide across row widths */
}

.tx-actions {
  margin-left: 20px;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #ef4444; /* Clean modern crimson tint */
  cursor: pointer;
  padding: 8px;
  font-size: 1.1rem;
  transition:
    transform 0.2s ease,
    color 0.2s ease;
}

.delete-btn:hover {
  color: #b91c1c; /* Deeper red on hover state */
  transform: scale(1.15); /* Subtle pop effect */
}

.amount {
  font-weight: 700;
  font-size: 1.1rem;
}

.amount.income {
  color: #4ade80;
}
.amount.expense {
  color: white;
  margin-bottom: 3px;
}

.date {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

.Side {
  position: fixed;
  top: 25px;
  left: 25px;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  z-index: 2000;
}

@media (max-width: 1024px) {
  .navItems {
    flex-wrap: wrap;
    gap: 8px;
  }

  .main-container.Shifted {
    padding: 0px;
    filter: blur(4px);
    pointer-events: none;
    transform: translateX(0px);
    transform: translateY(0px);
  }

  .SideBar {
    width: 65%;
  }

  .SideBar a {
    line-height: 2.5rem;
    font-size: 2.5vw;
  }
}

@media (max-width: 768px) {
  .navItems {
    gap: 6px;
  }

  .navItems a {
    padding: 4px 8px;
    font-size: 0.9rem;
  }

  .main-container {
    padding: 80px 15px 24px;
    max-width: 100%;
    overflow-x: hidden;
  }

  .main-container.Shifted {
    padding: 0px;
    filter: blur(4px);
    pointer-events: none;
  }

  .page-header {
    text-align: center;
  }

  .page-header h1 {
    font-size: 1.8rem;
  }

  .tx-card {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 12px;
    align-items: start;
    padding: 12px;
  }

  .tx-info {
    flex: 1 1 100%;
    margin-left: 0;
  }

  .tx-side-info {
    grid-column: 2;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    text-align: left;
    gap: 8px;
  }

  .tx-actions {
    grid-column: 2;
    margin-left: 0;
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}

@media (max-width: 480px) {
  .main-container {
    padding: 72px 12px 20px;
  }

  .tx-card {
    grid-template-columns: auto 1fr;
  }

  .tx-side-info {
    grid-column: 1 / -1;
    flex-direction: column;
    align-items: flex-start;
  }

  .tx-actions {
    grid-column: 1 / -1;
    justify-content: flex-start;
  }
}
</style>
