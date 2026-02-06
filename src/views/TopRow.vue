<script setup>
    import { RouterLink } from 'vue-router';
    import { ref, onMounted } from 'vue';
    import { Bar } from 'vue-chartjs'
    import { Line } from 'vue-chartjs';
    import {Chart as ChartJS, Title, Tooltip, Legend, LineElement, LineController, CategoryScale, LinearScale, PointElement, Filler, BarElement, BarController} from 'chart.js'

    ChartJS.register(Title, Tooltip, Legend, LineElement, LineController, CategoryScale, LinearScale, PointElement, Filler, BarElement, BarController)

    const isVisible = ref(false)
    const middleRowRef = ref(null);
    const tableRowRef = ref(null)
    const isIntersecting = ref(false);
    const isTableVisible = ref(false)

onMounted(() => {
    const observerOptions = {
        threshold: 0.4, 
        rootMargin: "0px 0px -50px 0px"
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
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
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4',],
        datasets: [{
            label: 'Spending',
            data: [380, 440, 500, 610],
            borderColor: '#818CF8',
            backgroundColor: 'rgba(129, 140, 248, 0.2)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#ffffff'
        }]
    }

    const chartData2 = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [{
            label: 'Monthly Average', 
            data: [2180, 2400, 2450, 2600, 2400, 2500, 3200, 3500, 4000, 3720, 3500, 4125],
            borderColor: '#818CF8',
            backgroundColor: 'rgba(129, 140, 248, 0.2)',
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: '#ffffff'
        }]
    }

    const ChartData3 = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'Subscriptions',
            data: [4, 4, 5, 6, 5, 3, 7, 5, 2, 6, 2, 7, 6],
            backgroundColor: '#818CF8',
            borderRadius: 8, 
            hoverBackgroundColor: '#ffffff'
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

    const chartOptions = {
        responsive: true, 
        maintainAspectRatio: false, 
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

    const tables = [
        {id:1, name: 'Netflix', value: '30$', status: 'Paid'},
        {id:2, name: 'Hulu', value: '20$', status: 'Pending'},
        {id:3, name: 'Spotify', value: '9.99$', status: 'Paid'},
        {id:4, name: 'Youtube Premium', value: '12$', status: 'Paid'},
        {id:5, name: 'ChatGpt Plus', value: '45$', status: 'Pending'},
    ]

    function toggleSiderbar() {
        isVisible.value = !isVisible.value;
    }
</script>

<template>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
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
        <div class="hero">
            <div class="Card1">
                <div class="chart-wrapper">
                    <Line :data="chartData" :options="chartOptions" />
                </div>
                <h2>Total Spent</h2>
                <p>Total amount spent for January is 1930$</p>
            </div>
            <div class="Card2">
                <div class="chart-wrapper">
                    <Line :data="chartData2" :options="chartOptions" />
                </div>
                <h2>Monthly average</h2>
                <p>Your monthly average is 2922.92$</p>
            </div>
            <div class="Card3">
                <div class="chart-wrapper">
                    <Bar :data="ChartData3" :options="chartOptions" />
                </div>
                <h2>Active Subscriptions</h2>
                <p>Current active subscription is 2</p>
            </div>
        </div>
        <div ref="middleRowRef" class="MiddleRow" :class="{ 'animate-trigger': isIntersecting }">
            <div class="middle-card">
                <div class="middle-chart-wrapper">
                    <Line :data="MidlleRowGraph" :options="chartOptions"></Line>
                </div>
                <h2>Deep Dive</h2>
                <p>Spending over last 6 months analysis.</p>
            </div>
        </div>
        <div class="bottomRow" ref="tableRowRef">
            <Transition name="fade">
                <table v-if="isTableVisible">
                    <thead>
                        <tr>
                            <th>Number</th>
                            <th>Subscriptions</th>
                            <th>Value</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <TransitionGroup name="list" tag="tbody" appear>
                        <tr v-for="( item, index ) in tables" :key="item.id" :style="{ transitionDelay: `${index * 0.1}s` }">
                            <td>{{ item.id }}</td>
                            <td>{{ item.name }}</td>
                            <td>{{ item.value }}</td>
                            <td>{{ item.status }}</td>
                        </tr>
                    </TransitionGroup>
                </table>
            </Transition>
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
        transition: all 0.6s ease-in-out;
        padding: 20px;
        box-sizing: border-box;
        overflow-x: hidden;
    }

    .main-container.Shifted {
        /* margin-left: 19%;
        width: 82%; */
        padding-left: 20%;
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
        z-index: 999;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
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

    .hero {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        gap: 20px;
        /* padding: 20px; */
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
        transition: all 0.6s ease-in-out;
        width: 100%;
        box-sizing: border-box;
        margin-bottom: 80px;
    }

    .Card1, .Card2, .Card3 {
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
    }

    .Card1:hover, .Card2:hover, .Card3:hover {
        transform: translateY(-15px);
        box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
    }

    .Card1 img, .Card2 img, .Card3 img{
        height: 35vh;
        width: 80%;
    }

    .chart-wrapper {
        width: 100%;
        height: 250px; /* Replaces your 35vh img height */
        margin-bottom: 20px;
        position: relative;
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

    .middle-card {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 30px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        height: 60vh;
        width: 100%;
        box-sizing: border-box;
    }

    .MiddleRow {
        width: 100%;
        padding: 0;
        box-sizing: border-box;
        opacity: 0;
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
    }

    .bottom-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        min-height: 100vh;
        transition: padding 0.6s ease-in-out; 
        padding: 20px;
        box-sizing: border-box;
        overflow-x: hidden;
    }

    .main-container.Shifted {
        padding-left: calc(17% + 40px);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        overflow: hidden;
        color: #ffffff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    th {
        background: rgba(129, 140, 248, 0.2);
        color: #818CF8;
        text-align: left;
        padding: 16px;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    td {
        padding: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.95rem;
    }

    tr:not(.list-enter-active):not(.list-appear-active) {
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    tr:last-child td {
        border-bottom: none;
    }

    tr:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: scale(1.01);
        cursor: pointer;
    }

    .Card1 { animation-delay: 0.1;}
    .Card2 { animation-delay: 0.1;}
    .Card3 { animation-delay: 0.1;}
    .animate-trigger { animation: SideEnter 1.5s ease-out forwards;}

    @media (max-width: 768px) {
        /* 1. Stack the Top Cards */
        .hero {
            flex-direction: column;
            margin-bottom: 40px;
            gap: 30px;
        }

        .Card1, .Card2, .Card3 {
            width: 90%;
            height: auto; /* Let height be determined by content */
            min-height: 350px;
            padding: 25px;
        }

        /* 2. Fix the Sidebar for Mobile */
        .SideBar {
            width: 70%; /* Wider on mobile for readability */
            height: 100vh;
            margin: 0;
            border-radius: 0 16px 16px 0;
            backdrop-filter: blur(15px); /* Stronger blur for overlay */
        }

        /* 3. Handle Content Shifting */
        .main-container {
            padding-top: 60px; /* Room for the menu icon */
        }

        .main-container.Shifted {
            padding-left: 20px; /* Don't push content off-screen on mobile */
            opacity: 0.3; /* Optional: dim content when menu is open */
            filter: blur(2px);
        }

        /* 4. The Middle Card (Deep Dive) */
        .middle-card {
            height: auto;
            padding: 20px;
        }

        .middle-chart-wrapper {
            height: 300px; /* Slightly smaller for mobile screens */
        }

        /* 5. Responsive Table */
        .bottomRow {
            padding: 10px;
            overflow-x: auto; /* Critical: allows table to swipe left/right */
            display: block; /* Changes from flex to block for scrolling */
        }

        table {
            min-width: 600px; /* Forces table to stay wide enough to read */
            margin-bottom: 20px;
            border-radius: 8px; /* Slightly smaller radius for mobile */
        }

        th, td {
            padding: 12px 10px; /* Tighter padding for mobile screens */
            font-size: 0.85rem;
        }

        /* Adjust typography for smaller screens */
        h2 {
            font-size: 1.25rem;
        }

        p {
            font-size: 0.85rem;
        }
    }
</style>