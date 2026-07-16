<script setup>
import { RouterLink } from "vue-router";
import { ref } from "vue";
import axios from "axios";

const isVisible = ref(false);
const income1 = ref(500);
const income2 = ref(500);
const income3 = ref(500);

// Reactive state flags for showing success notifications
const showExtraSuccess = ref(false);
const showSubSuccess = ref(false);
const showTxSuccess = ref(false);

const extraData = ref({
  monthly_contributed: null,
  debt_contributions: null,
  emergency_contributions: null,
  subscription_name: "",
  subscription_price: "",
  subscription_status: "",
  transaction_name: "",
  transaction_value: "",
  transaction_date: "",
});

const formatCurrency = (val) => {
  const displayVal = val !== null ? val : 500;
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(displayVal);
};

const sendData = async () => {
  try {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("No authorization token found. Please log in first.");
      return;
    }

    // Determine which sections the user actually filled out before we reset the state
    const hasExtraInfo =
      extraData.value.monthly_contributed !== null ||
      extraData.value.debt_contributions !== null ||
      extraData.value.emergency_contributions !== null;

    const hasSubscription = extraData.value.subscription_name.trim() !== "";
    const hasTransaction = extraData.value.transaction_name.trim() !== "";

    // Sanitize data before sending
    const payload = {
      ...extraData.value,
      monthly_contributed: extraData.value.monthly_contributed ?? 0,
      debt_contributions: extraData.value.debt_contributions ?? 0,
      emergency_contributions: extraData.value.emergency_contributions ?? 0,
      subscription_price:
        extraData.value.subscription_price === ""
          ? 0
          : Number(extraData.value.subscription_price),
      transaction_value:
        extraData.value.transaction_value === ""
          ? 0
          : Number(extraData.value.transaction_value),
    };

    const response = await axios.post(
      "https://yassinafify.pythonanywhere.com/settings",
      payload,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    console.log("Settings updated:", response.data);

    // Trigger success banners only for the filled sections
    if (hasExtraInfo) {
      showExtraSuccess.value = true;
      setTimeout(() => {
        showExtraSuccess.value = false;
      }, 4000);
    }
    if (hasSubscription) {
      showSubSuccess.value = true;
      setTimeout(() => {
        showSubSuccess.value = false;
      }, 4000);
    }
    if (hasTransaction) {
      showTxSuccess.value = true;
      setTimeout(() => {
        showTxSuccess.value = false;
      }, 4000);
    }

    // Reset state inputs
    extraData.value = {
      monthly_contributed: null,
      debt_contributions: null,
      emergency_contributions: null,
      subscription_name: "",
      subscription_price: "",
      subscription_status: "",
      transaction_name: "",
      transaction_value: "",
      transaction_date: "",
    };
  } catch (error) {
    console.error("Error saving data:", error.response?.data || error.message);
  }
};
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

  <div class="navBar">
    <div class="navItems">
      <RouterLink to="/Home" class="navItem">Home</RouterLink>
      <RouterLink to="/Transactions" class="navItem">Transactions</RouterLink>
      <RouterLink to="/Reports" class="navItem">Reports</RouterLink>
      <RouterLink to="/Settings" id="current" class="navItem"
        >Settings</RouterLink
      >
    </div>
  </div>
  <div class="main-container" :class="{ shifted: isVisible }">
    <div class="titleContainer">
      <h3>Extra Info</h3>
    </div>
    <div class="countersContainer">
      <div class="counters">
        <div class="salaryCard">
          <div class="top">
            <p>Monthly Contributed</p>
            <span class="value-display">{{
              formatCurrency(extraData.monthly_contributed)
            }}</span>
          </div>
          <div class="mid">
            <input
              v-model.number="extraData.monthly_contributed"
              type="range"
              min="500"
              max="7500"
              step="100"
            />
          </div>
          <div class="bot">
            <p>$500</p>
            <p>Your savings Contributions this month</p>
            <p>$7,500</p>
          </div>
        </div>
        <div class="salaryCard">
          <div class="top">
            <p>Debt Contributions</p>
            <span class="value-display">{{
              formatCurrency(extraData.debt_contributions)
            }}</span>
          </div>
          <div class="mid">
            <input
              v-model.number="extraData.debt_contributions"
              type="range"
              min="500"
              max="7500"
              step="100"
            />
          </div>
          <div class="bot">
            <p>$500</p>
            <p>Your Contributions towards paying off your debts this month</p>
            <p>$7,500</p>
          </div>
        </div>
        <div class="salaryCard">
          <div class="top">
            <p>Emergency Contributions</p>
            <span class="value-display">{{
              formatCurrency(extraData.emergency_contributions)
            }}</span>
          </div>
          <div class="mid">
            <input
              v-model.number="extraData.emergency_contributions"
              type="range"
              min="500"
              max="7500"
              step="100"
            />
          </div>
          <div class="bot">
            <p>$500</p>
            <p>Your Contributions towards your emergency fund this month</p>
            <p>$7,500</p>
          </div>
        </div>
      </div>
      <p v-if="showExtraSuccess" class="successExtraInfo">
        Success! View your updated info in the home page
      </p>
    </div>

    <div class="subs">
      <h3>Add Subscriptions</h3>
      <div class="inputsContainer">
        <div class="inputs">
          <input
            v-model="extraData.subscription_name"
            type="text"
            placeholder="Subscription Name"
          />
          <input
            class="subscriptionPrice"
            v-model="extraData.subscription_price"
            type="number"
            placeholder="Price"
          />
          <input
            v-model="extraData.subscription_status"
            type="text"
            placeholder="Status"
          />
        </div>
      </div>

      <p v-if="showSubSuccess" class="subscriptionSuccessInfo">
        Success! View your subscription in the home page
      </p>
    </div>
    <div class="subs">
      <h3>Add Transactions</h3>
      <div class="inputsContainer2">
        <div class="inputs">
          <input
            v-model="extraData.transaction_name"
            type="text"
            placeholder="Transaction Name"
          />
          <input
            class="transactionPrice"
            v-model="extraData.transaction_value"
            type="number"
            placeholder="Value"
          />
          <input
            v-model="extraData.transaction_date"
            type="date"
            placeholder="Date"
          />
        </div>
      </div>

      <div v-if="showTxSuccess" class="transactionSuccessInfo">
        Success! View your transaction in the transactions page
      </div>
    </div>
    <div class="saveContainer">
      <button @click="sendData" class="save">Save</button>
    </div>
  </div>
</template>

<style scoped>
/* ==========================================================================
       ANIMATIONS & TRANSITIONS
       ========================================================================== */
/* @keyframes fallIn {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }
     
    @keyframes SideEnter {
        from {
            opacity: 0;
            transform: translateX(-100px);
        }
        to {
            opacity: 1;
            transform: translateX(0px);
        }
    }

    @keyframes SideEnterRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0px);
        }
    } */

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* ==========================================================================
       BASE DESKTOP LAYOUT
       ========================================================================== */
.main-container {
  width: 100%;
  box-sizing: border-box;
  padding: 40px;
  /* transition: all 0.5s ease; */
}

.main-container.shifted {
  margin-left: 270px;
  width: calc(100% - 270px);
}

.titleContainer {
  padding-top: 40px;
  margin-bottom: 20px;
}

.subs h3,
.main-container h3 {
  color: #ffffff;
  font-size: 2rem;
  font-family: "Plus Jakarta Sans", sans-serif;
  margin-bottom: 20px;
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

.a {
  padding: 10px 20px;
  margin: 0 10px;
  text-decoration: none;
  color: #818cf8;
  border-radius: 8px;
  /* transition: all 0.3s ease; */
}

.a:hover {
  color: #ffffff;
}

.toggle-btn-container {
  position: fixed;
  top: 25px;
  left: 25px;
  z-index: 1000;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  /* transition: all 0.5s ease-in-out; */
}

.countersContainer {
  display: flex;
  flex-direction: column; /* Stacks .counters and the p tag vertically */
  align-items: center; /* Keeps them centered horizontally */
  width: 100%;
  margin-bottom: 40px;
}

.counters {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 20px;
  width: 100%; /* Spans the full width of the container */
}

.salaryCard {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
  padding: 20px;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.top p {
  font-family: Manrope, sans-serif;
  color: rgb(163, 163, 181);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 0.75rem;
  margin: 0;
}

.top span {
  font-family:
    JetBrains mono,
    monospace;
  color: rgba(163, 163, 181, 1);
  font-weight: 600;
  font-size: 1.125rem;
}

.mid {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 15px 0;
}

.mid input {
  appearance: none;
  cursor: pointer;
  width: 100%;
  height: 3px;
  background: #2a2a45;
  outline: none;
}

.bot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 10px;
}

.bot p {
  font-family:
    JetBrains Mono,
    monospace;
  font-size: 10px;
  color: rgb(163, 163, 181);
  margin: 0;
}

.bot p:nth-child(2) {
  text-align: center;
  max-width: 60%;
}

/* ==========================================================================
       INPUT FORM FIELDS
       ========================================================================== */
.inputsContainer,
.inputsContainer2 {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 40px;
}

/* .inputsContainer { animation: SideEnterRight 1s ease-in-out; } */
/* .inputsContainer2 { animation: SideEnter 1s ease-in-out; } */

.inputs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;
  gap: 20px;
  width: 100%;
  padding: 20px;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-sizing: border-box;
}

.inputs input {
  flex: 1;
  height: 45px;
  padding: 0 15px;
  background: rgba(255, 255, 255, 0.025);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  box-sizing: border-box;
}

/* ==========================================================================
       SAVE BUTTON
       ========================================================================== */
.saveContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.save {
  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 12px 40px;
  color: #ffffff;
  cursor: pointer;
  /* transition: all 0.2s ease-in-out; */
  font-family:
    DM Sans,
    sans-serif;
  font-weight: 500;
  font-size: 1rem;
}

.save:hover {
  transform: translateY(-3px);
  box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
}

.subscriptionSuccessInfo,
.transactionSuccessInfo {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: rgb(0, 200, 83);
}

.successExtraInfo {
  margin-top: 20px; /* Adds space between the bottom of the cards and the text */
  width: 100%; /* Forces the block line-break */
  text-align: center;
  color: rgb(0, 200, 83);
}

/* ==========================================================================
       RESPONSIVE BREAKPOINTS
       ========================================================================== */
@media (max-width: 1024px) {
  .main-container,
  .main-container.shifted {
    margin-left: 0;
    width: 100%;
    max-width: 100vw;
    padding: 20px;
    overflow-x: hidden; /* Prevents layout leaks from parent container */
  }

  .toggle-btn-container.shifted {
    transform: translateX(0px);
    z-index: 1001;
  }

  .SideBar {
    display: flex;
    justify-content: space-around;
    width: 340px;
    height: 100vh;
    margin: 0;
    border-radius: 0 16px 16px 0;
    background: rgba(15, 23, 42, 0.95);
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
  }

  .counters,
  .inputs {
    width: 100%; /* Uses full available flex space instead of breaking layout boundaries */
    max-width: 100%;
  }

  .inputs input {
    padding: 7px;
  }
}

@media (max-width: 1024px) {
  .navItems {
    flex-wrap: wrap;
    gap: 8px;
  }

  .main-container,
  .main-container.shifted {
    margin-left: 0;
    width: 100%;
    max-width: 100vw;
    padding: 20px;
    overflow-x: hidden;
    box-sizing: border-box;
  }

  .counters,
  .inputs {
    width: 100%;
    max-width: 100%;
  }

  .inputs input {
    padding: 7px;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 20px 14px 32px;
  }

  .titleContainer {
    padding-top: 32px;
    text-align: center;
  }

  .subs h3,
  .main-container h3 {
    font-size: 1.35rem;
    text-align: center;
    margin: 20px 0;
  }

  .counters {
    flex-direction: column;
    gap: 12px;
    width: 100%;
  }

  .salaryCard {
    width: 100%;
    box-sizing: border-box;
    padding: 16px;
  }

  .top {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .bot {
    flex-direction: row;
    align-items: flex-start;
    gap: 6px;
  }

  .inputs {
    flex-direction: column;
    gap: 12px;
    width: 100%;
    padding: 14px;
  }

  .inputs input {
    width: 100%;
    max-width: 100%;
    height: 44px;
    padding: 7px;
  }

  .saveContainer {
    width: 100%;
    padding: 0 15px;
    box-sizing: border-box;
  }

  .save {
    width: 100%;
  }

  .toggle-btn-container {
    left: auto;
    right: 25px;
    top: 25px;
    z-index: 1001;
  }

  .toggle-btn-container.shifted {
    transform: none;
  }

  .SideBar {
    position: fixed;
    left: 0;
    top: 0;
    width: 80vw;
    height: 100vh;
    margin: 0;
    border-radius: 0;
    background: rgba(255, 255, 255, 0.025);
    border: none;
    z-index: 1000;
    padding: 0;
    display: flex;
    align-items: flex-start;
    justify-content: space-evenly;
    border-radius: 16px;
    padding-left: 10px;
  }
}

@media (max-width: 480px) {
  .navItems {
    justify-content: center;
  }

  .navItems a {
    margin: 4px;
    font-size: 0.9rem;
  }

  .main-container {
    padding: 16px 12px 24px;
  }

  .titleContainer {
    padding-top: 24px;
  }

  .top p {
    font-size: 0.7rem;
  }

  .top span {
    font-size: 1rem;
  }

  .inputs {
    padding: 12px;
  }

  .inputs input {
    height: 42px;
    padding: 7px;
  }

  .save {
    width: 100%;
  }
}
</style>
