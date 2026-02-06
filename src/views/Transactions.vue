<script setup>
    import { ref } from 'vue';
    const isVisible = ref(false)

    function toggleSiderbar() {
        isVisible.value = !isVisible.value;
    }

    const transactions = ref([
        {id: 1, name: 'Amazon', category: 'Shopping', amount: 84.99, date: 'Feb 05', icon: 'fa-bag-shopping', type: 'expense'},
        {id: 2, name: 'Starbucks', category: 'Food & Drinks', amount: 12.50, date: 'Feb 04', icon: 'fa-mug-hot', type: 'expense'},
        {id: 3, name: 'Salary Deposit', category: 'Income', amount: 2600, date: 'Feb 01', icon: 'fa-wallet', type: 'income'},
        {id: 4, name: 'Netflix', category: 'Entertainment', amount: 15.99, date: 'Jan 28', icon: 'fa-play', type: 'expense'},
    ])
</script>

<template>
    
    <component is="style">
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    </component>

    <div class="Side" id="side">
        <i class="fa-solid fa-bars" id="icon" @click="toggleSiderbar" style="margin-left: 15px; margin-top: 20px"></i>
    </div>
    <Transition name="slide">
        <div class="SideBar" id="SideBar" v-show="isVisible">
            <RouterLink to="/" class="a">Home</RouterLink>
            <RouterLink to="/Transactions" class="a">Transactions</RouterLink>
            <RouterLink to="/Reports" class="a">Reports</RouterLink>
            <RouterLink to="/Settings" class="a">Settings</RouterLink>
        </div>
    </Transition>

    <div class="main-container" :class="{'Shifted' : isVisible}">
        
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
                        {{ tx.type === "expense" ? '-' : '+'}}${{ tx.amount.toFixed(2) }}
                    </span>
                    <span class="date">{{ tx.date }}</span>
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
        font-family: 'Plus Jakarta Sans', sans-serif;
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
            transform: translateY(300px);
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
        color: #818CF8;
        z-index: -1;
    }

    .a:hover {
        color: #ffffff;
        text-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
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
        z-index: 1500;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
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
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
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

    .tx-icon-wrapper.expense { background: rgba(255, 255, 255, 0.1); color: white; }
    .tx-icon-wrapper.income { background: rgba(74, 222, 128, 0.2); color: #4ade80; }

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

    .amount {
        font-weight: 700;
        font-size: 1.1rem;
    }

    .amount.income { color: #4ade80; }
    .amount.expense { color: white; }

    .date {
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.4);
    }

    .Side {
        position: fixed;
        top: 20px;
        left: 20px;
        color: white;
        cursor: pointer;
        z-index: 2000;
    }

    @media (max-width: 768px) {
        .SideBar {
            width: 75%; /* More width on mobile for easier tapping */
            height: 100%;
            margin: 0;
            border-radius: 0 16px 16px 0;
            z-index: 100; /* Ensure it stays on top */
        }

        .main-container {
            padding: 80px 15px 20px 15px; /* More room for the hamburger icon */
        }

        /* On mobile, we DON'T shift the container, we just blur it */
        .main-container.Shifted {
            padding-left: 15px; 
            filter: blur(4px);
            pointer-events: none; /* Prevent clicking transactions while menu is open */
        }

        .page-header h1 {
            font-size: 1.8rem;
        }

        .tx-card {
            padding: 12px; /* Tighter padding for smaller screens */
        }
    }
</style>