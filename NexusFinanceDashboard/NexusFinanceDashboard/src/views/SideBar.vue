<script setup>
    // import { RouterLink } from 'vue-router';
    // import { ref } from 'vue';
    // const isVisible = ref(false)

    // function toggleSiderbar() {
    //     isVisible.value = !isVisible.value;
    // }

</script>

<template>
    <!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <div class="Side" id="side">
        <i class="fa-solid fa-bars" id="icon" @click="toggleSiderbar" style="margin-left: 10px; margin-top: 15px; z-index: 101;"></i>
    </div>
    <Transition name="slide">
        <div class="SideBar" id="SideBar" v-show="isVisible">
            <RouterLink to="/" class="a">Home</RouterLink>
            <RouterLink to="/Transactions" class="a">Transactions</RouterLink>
            <RouterLink to="/Reports" class="a">Reports</RouterLink>
            <RouterLink to="/Settings" class="a">Settings</RouterLink>
        </div>
    </Transition> -->
</template>

<style scoped>
    /* .slide-enter-active,
    .slide-leave-active {
      transition: all 0.6s ease-in-out;
    }

    .slide-enter-from,
    .slide-leave-to {
      transform: translateX(-100%); 
      opacity: 0;
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
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        position: fixed;
        left: 0;
        top: 0;
        z-index: 100;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
    }

    .a {
        margin: 20px;
        overflow: hidden;
        text-decoration: none;
        color: #818CF8;
    }

    .a:hover {
        color: #ffffff;
        text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
    } */
</style>