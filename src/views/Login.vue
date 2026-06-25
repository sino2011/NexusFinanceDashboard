<script setup>
import { ref } from "vue";
import axios from "axios";
import router from "@/router/router";

const data = ref({
  email: null,
  password: null,
});
const error = ref(null);

const submitData = async () => {
  error.value = null;

  try {
    const response = await axios.post(
      "https://yassinafify.pythonanywhere.com/login",
      data.value,
    );
    if (response.data?.message === "Login successful") {
      router.push({ name: "Home" });
    } else {
      error.value = response.data?.error || "Login failed";
    }
  } catch (err) {
    error.value = err.response?.data?.error || "Unable to login";
  }
};
</script>
<template>
  <div class="login">
    <div class="main">
      <div class="inputContainer">
        <h2>Login</h2>
        <form @submit.prevent="submitData">
          <div class="field">
            <p>Email:</p>
            <input
              v-model="data.email"
              type="email"
              placeholder="John@gmail.com"
            />
          </div>
          <div class="field">
            <p>Password:</p>
            <input v-model="data.password" type="password" placeholder="" />
          </div>
          <button>Login</button>
          <p class="error" v-if="error">{{ error }}</p>
          <p class="register">
            Dont Have an Account?
            <a href="/NexusFinanceDashboard/#/signUp">Register</a>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>
<style scoped>
* {
  margin: 0px;
  padding: 0px;
  box-sizing: border-box;
}

.login {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.main {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  min-height: 100vh;
  padding: 24px;
}

.inputContainer {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  overflow: hidden;
  width: min(100%, 520px);
  min-height: 50vh;
  background: rgb(34 34 61);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  gap: 24px;
  padding: 32px 24px;
}

form {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 20px;
  width: 100%;
}

.inputContainer button {
  border-radius: 100px;
  padding: 10px 20px;
  cursor: pointer;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  color: #f0f0f0;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform: translateY(3px);
  width: 100%;
}

.inputContainer h2 {
  color: #f0f0f0;
}

button:hover {
  transform: translateY(-5px);
  box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
}

.field {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
}

.field p {
  color: rgb(163 163 181);
  font-family:
    JetBrains Mono,
    monospace;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  font-size: 14px;
  min-width: 70px;
}

.field input {
  border-radius: 0.75rem;
  padding: 10px 16px;
  text-decoration: none;
  box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.1);
  font-family: Manrope, sans-serif;
  color: rgb(255, 255, 255);
  background-color: rgba(26, 26, 46, 1);
  font-size: 0.875rem;
  line-height: 1.25rem;
  border-color: rgba(163, 163, 181, 0.2);
  border-width: 1px;
  width: 100%;
}

.register {
  color: rgb(255, 255, 255);
  text-align: center;
}

.error {
  color: #f87171;
  font-size: 0.95rem;
  text-align: center;
}

a {
  text-decoration: none;
  color: #818cf8;
}

@media (max-width: 768px) {
  .main {
    padding: 16px;
  }

  .inputContainer {
    padding: 24px 16px;
    gap: 20px;
    min-height: auto;
  }

  .field {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .field p {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .main {
    padding: 12px;
  }

  .inputContainer {
    padding: 20px 14px;
    border-radius: 14px;
  }

  .register {
    font-size: 0.95rem;
    line-height: 1.5;
  }
}
</style>
