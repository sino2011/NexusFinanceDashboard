<script setup>
    import { Bar } from 'vue-chartjs'
    import { Line } from 'vue-chartjs';
    import { Doughnut } from 'vue-chartjs';
    import {Chart as ChartJS, Title, Tooltip, Legend, LineElement, LineController, CategoryScale, LinearScale, PointElement, Filler, BarElement, BarController, ArcElement, DoughnutController} from 'chart.js'
    import { ref } from 'vue';
    
    ChartJS.register(Title, Tooltip, Legend, LineElement, LineController, CategoryScale, LinearScale, PointElement, Filler, BarElement, BarController, ArcElement, DoughnutController)
    
    const isVisible = ref(false)
    
    function toggleSiderbar() {
        isVisible.value = !isVisible.value;
    }
    const SavingsData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Savings',
            data: [12, 17, 15, 24, 19, 14, 20, 21, 18, 16, 22, 26,],
            borderColor: '#4ADE80',
            backgroundColor: 'rgba(74, 222, 128, 0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 0,
            pointBackgroundColor: '#ffffff'
        }]
    }

    const donutData = {
        labels: ['Food', 'Rent', 'Entertainment', 'Others'],
        datasets: [{
          backgroundColor: ['#4ADE80', '#818CF8', '#FBBF24', '#F87171'],
          data: [40, 30, 20, 10],
          borderWidth: 0,
          hoverOffset: 10
        }]
    }

    const MidlleRowGraph = {
        labels: ['July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label:'Spendings over last 6 months',
            data: [2950, 3000, 3650, 3420, 3120, 3920],
            borderColor: '#818CF8',
            backgroundColor: 'rgba(129, 140, 248, 0.2)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#ffffff'
        }]
    }

    const sparklineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: true }
        },
        scales: {
            x: { display: false }, 
            y: { 
                display: false, 
                beginAtZero: true 
            }
        },
        elements: {
            line: {
                borderWidth: 2,
                tension: 0.4
            },
            point: { radius: 0 } 
        }
    }

    const chartOptions = {
        responsive: true, 
        maintainAspectRatio: false,
        resizeDelay: 0,
        animation: {
            duration: 400
        },
        plugins: {
            legend: {display: false}
        },
        scales: {
            y: {
                beginAtZero : true,
                grid: {color: 'rgba(255, 255, 255, 0.1)'},
                ticks: {color: 'rgba(255, 255, 255, 0.7)'}
            },
            x: {
                grid: {display: false},
                ticks: {color: 'rgba(255, 255, 255, 0.7)'}
            }
        }
    }

    const donutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%', // This creates the "Donut" hole. Higher = thinner ring.
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
            labels: { color: '#ffffff', padding: 20 }
          }
        }
    }
</script>

<template>

    <component is="style">
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    </component>

    <div class="app-layout">
        <div class="toggle-btn-container" :class="{'shifted' : isVisible}">
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
        <div class="content-view">
        
            <div class="mainContainer">
                <div class="Cards">
                    <div class="Total">
                        <h2>Total Balance</h2>
                        <p>Your total net worth: 5400$</p>
                    </div>
                    <div class="Savings">
                        <div class="chartContainer">
                            <Line :data="SavingsData" :options="chartOptions"></Line>
                        </div>
                        <h2>Savings Rate</h2>
                        <p>Your savings rate is 24%, Great job!</p>
                    </div>
                    <div class="topSpending">
                        <h2>Top Spending</h2>
                        <p>Your top spending category is " Food & Drinks "</p>
                    </div>
                </div>
                <div class="Core">
                    <div class="left">
                      <div class="middle-card">
                            <div class="middle-chart-wrapper">
                                <Line :data="MidlleRowGraph" :options="chartOptions" />
                            </div>
                            <h2>Deep Dive</h2>
                            <p>Spending over last 6 months analysis.</p>
                        </div>
                    </div>
                
                    <div class="Right">
                        <div class="Donut-card">
                            <div class="middle-chart-wrapper">
                                <Doughnut :data="donutData" :options="donutOptions" />
                            </div>
                        </div>
                    </div>
            </div>
          </div>
        </div>
    </div>
    
</template>

<style scoped>
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

    .slide-enter-active,
    .slide-leave-active {
      transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .slide-enter-from,
    .slide-leave-to {
        flex: 0 0 0px; /* Shrink the sidebar space to zero */
        margin: 0;
        width: 0;
        opacity: 0;
        transform: translateX(-20px);
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

    .app-layout {
        display: flex;
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: #0f172a; /* Dark background to match your glass theme */
        overflow: hidden; /* Prevents unwanted scrollbars during animation */
        font-family: 'Plus Jakarta Sans', sans-serif;
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
    }

    /* Move the button slightly when sidebar is open if you want */
    .toggle-btn-container.shifted {
        transform: translateX(10px); 
    }

    .SideBar {
        display: flex;
        flex: 0 0 250px;
        flex-direction: column;
        justify-content: space-around;
        height: calc(100vh - 20px);
        margin: 10px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(5px);
        z-index: 1;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
        overflow: hidden; 
        white-space: nowrap;
    }

    .content-view {
        flex: 1; /* Automatically fills remaining space */
        display: flex;
        flex-direction: column;
        overflow-y: auto; /* Allow vertical scroll if content is tall */
        min-width: 0; /* CRITICAL for Chart.js to resize smaller */
        padding-bottom: 30px;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .Cards {
        display: flex; /* Grid is much more reliable for sizing */
        gap: 20px;
        width: 100%;
        margin-top: 20px;
    }

    .Total, .Savings, .topSpending {
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
        height: 55vh;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        transform: translateY(20px);
        animation: fallIn 2s ease-in-out forwards;
        opacity: 0;
        padding: 20px;
        position: relative;
    }

    .Total:hover, .topSpending:hover, .Savings:hover {
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
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 30px; /* Space between Row 1 and Row 2 */
        overflow-x: hidden;
        min-width: 0
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
        flex: 0 0 60%; 
        min-width: 0;
        display: flex;
    }
    
    /* The 40% side (rest of space) */
    .Right {
        flex: 1; 
        min-width: 0;
        display: flex;
    }
    
    /* Glass Card Styling for Middle Row */
    .middle-card, .Donut-card {
        width: 100%;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
        animation: SideEnter 2s ease forwards;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .middle-card:hover, .Donut-card:hover {
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

    .animate-trigger { animation: SideEnter 1.5s ease-out forwards;}

    @media (max-width: 768px) {
        /* 1. Adjust Layout Flow */
        .Cards {
            flex-direction: column; /* Stack the 3 top cards */
        }
    
        .Core {
            flex-direction: column; /* Stack the Deep Dive and Donut cards */
            height: auto; /* Allow height to grow with content */
        }
    
        .left, .Right {
            flex: 1 1 100%; /* Take full width on mobile */
        }
    
        /* 2. Adjust Card Heights */
        .Total, .Savings, .topSpending {
            height: 250px; /* Reduce height so user doesn't have to scroll forever */
            padding: 15px;
        }

        .chartContainer {
            display: none;
        }
    
        .middle-card, .Donut-card {
            height: 400px; /* Specific height for charts on mobile */
            padding: 20px;
        }
    
        /* 3. Handle Sidebar on Mobile */
        .SideBar {
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            width: 80%; /* Sidebar covers most of the screen on mobile */
            max-width: 300px;
            margin: 0;
            border-radius: 0 16px 16px 0;
        }
    
        .mainContainer {
            padding: 15px;
            padding-top: 80px; /* Give room for the floating menu button */
        }
    
        /* 4. Text scaling */
        h2 {
            font-size: 1.2rem;
        }
    
        p {
            font-size: 0.85rem;
        }
    }
</style>