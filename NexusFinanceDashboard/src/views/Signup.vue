<script setup>
    import { ref, onMounted } from 'vue';
    import axios from 'axios';
    import router from '@/router/router';
    
    const income1 = ref(20000);
    const income2 = ref(20000);
    const timeline = ref(12);
    const income3 = ref(5000);
    const income4 = ref(1000);
    const isLightMode = ref(false);
    const isVisible = ref(false);
    const isMiddleRowIntersecting = ref(false);
    const isTableRowIntersecting = ref(false);
    const tableRowRef = ref(null);
    const middleRowRef = ref(null);
    const targetElement = ref(null);
    const users = ref([])
    const loading = ref(true)
    const formData = ref({
        first_name: null,
        last_name: null,
        date_birth: null,
        passw: null,
        mail: null,
        annual_income: 20000,
        savings_target: 20000,
        timeline: 12,
        total_savings: 5000,
        emergency_fund: 1000
    })

    const statusMessage = ref('')

    const submitData = async () => {
        if (!formData.value.first_name || !formData.value.last_name || !formData.value.mail || !formData.value.passw) {
            statusMessage.value = 'Please fill out all required fields.'
            return;
        }
        statusMessage.value = 'Savings data...'
        try {
            const response = await axios.post('http://localhost:5000/api/calculate', formData.value)
            statusMessage.value = response.data.message

            localStorage.setItem('nexus_user_registered', 'true')
            router.push("/Home")   

            formData.value = {first_name: '', last_name: '', date_birth: '', passw: '', mail: '', annual_income:20000, savings_target:20000, timeline:12, total_savings:5000, emergency_fund:1000}
        } catch(error) {
            console.error('Error saving data:', error)
            statusMessage.value = 'Failed to save data. Check backend logs.'
            if (error.response && error.response.data && error.response.data.message) {
                statusMessage.value = error.response.data.message
            }else{
                statusMessage.value = 'An unexpected error occurred. Please try again.'
            }
        }

    }

    const formatCurrency = (val) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0
      }).format(val);
    };

    const formatTime = (val) => {
        return new Intl.NumberFormat('en-US', {
            style: 'unit',
            unit: 'month',
            unitDisplay: 'long',
            maximumFractionDigits: 0
        }).format(val);
    };

    const scrollToSection = () => {
        targetElement.value?.scrollIntoView({behavior : 'smooth'})
    }

    const toggleTheme = () => {
        isLightMode.value = !isLightMode.value;
    };

    onMounted(() => {
        // A single observer options configuration that covers both cases nicely
        const observerOptions = {
            threshold: [0.5, 0.3], // Listens for both 50% and 100% visibility thresholds
            rootMargin: "0px 0px -50px 0px"
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Check if it's the middle row passing 50% visibility
                    if (entry.target === middleRowRef.value && entry.intersectionRatio >= 0.5) {
                        isMiddleRowIntersecting.value = true;
                        observer.unobserve(entry.target); // Stop tracking once triggered
                    }
                    
                    // Check if it's the table row passing 100% visibility
                    if (entry.target === tableRowRef.value && entry.intersectionRatio >= 0.1) {
                        isTableRowIntersecting.value = true;
                        observer.unobserve(entry.target); // Stop tracking once triggered
                    }
                }
            });
        }, observerOptions);

        // Tell our single observer to watch both elements
        if (middleRowRef.value) observer.observe(middleRowRef.value);
        if (tableRowRef.value) observer.observe(tableRowRef.value);

        // fetchUsers()
    });
</script>

<template>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Manrope:wght@200..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" integrity="sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">

    
    <div class="personal">
        <div class="topRow">
            <div class="titleContainer">
                <h1 class="title">Welcome to Nexus</h1>
            </div>
            <div class="feat">
                <div class="feat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" width="14" height="14" class=" text-[#00C853]"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"></path></svg>
                    <span>Your 3-strategy comparison table</span>
                </div>
               <div class="feat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" width="14" height="14" class=" text-[#00C853]"><path stroke-linecap="round" stroke-linejoin="round" d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"></path></svg>
                    <span>Milestone calendar with excat dates</span>
                </div>
                <div class="feat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" width="14" height="14" class=" text-[#00C853]"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5"></path></svg>
                    <span>Automation setup checklist</span>
                </div>
                <div class="feat-item">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" aria-hidden="true" data-slot="icon" width="14" height="14" class=" text-[#00C853]"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"></path></svg>
                    <span>Rate optimization worksheet</span>
                </div>
            </div>
            <div class="form-content">
                <div class="para">
                    <label>First Name</label>
                    <label>Last Name</label>
                    <label>Date of birth</label>
                    <label>Set a password</label>
                    <label>Email address</label>
                </div>
                <form @submit.prevent="submitData">
                    <div class="inputs">
                        <input v-model="formData.first_name" type="text" class="firstName" placeholder="Alex">
                        <input v-model="formData.last_name" type="text" class="lastName" placeholder="Adam">
                        <input v-model="formData.date_birth" type="date" class="date">
                        <input v-model="formData.passw" type="password">
                        <input v-model="formData.mail" type="email" placeholder="alex@gmail.com">
                    </div>
                </form>
            </div>
            <div v-if="statusMessage" :class="['status-msg', { 'error-msg': statusMessage.includes('Failed') || statusMessage.includes('exists') || statusMessage.includes('fill') }]">
                {{ statusMessage }}
            </div>
            <button @click="scrollToSection" type="submit">Run your numbers</button>
        </div>
        
        <div class="countersContainer" ref="middleRowRef" >
                <h2>Your numbers, Three ways.</h2>
                <p class="adj">Adust income, target and timeline</p>
                <form @submit.prevent="submitData">
                    <div class="counters" ref="targetElement" :class="{ 'animate-trigger': isMiddleRowIntersecting }">
                        <div class="salaryCard">
                            <div class="top">
                                <p>Annual Income</p>
                                <span class="value-display">{{ formatCurrency(income1) }}</span>
                            </div>
                            <div class="mid">
                                <input v-model.number="income1" @input="formData.annual_income = income1" type="range" min="20000" max="500000" step="1000" required>
                            </div>
                            <div class="bot">
                                <p>$20,000</p>
                                <p>$500,000</p>
                            </div>
                        </div>
                        <div class="salaryCard">
                            <div class="top">
                                <p>Savings Target</p>
                                <span class="value-display">{{ formatCurrency(income2) }}</span>
                            </div>
                            <div class="mid">
                                <input v-model.number="income2" @input="formData.savings_target = income2" type="range" min="20000" max="500000" step="1000" required>
                            </div>
                            <div class="bot">
                                <p>$20,000</p>
                                <p>Emergency fund, vacation, down payment</p>
                                <p>$500,000</p>
                            </div>
                        </div>
                        <div class="salaryCard">
                            <div class="top">
                                <p>Your timeline</p>
                                <span class="value-display">{{ formatTime(timeline) }}</span>
                            </div>
                            <div class="mid">
                                <input v-model.number="timeline" @input="formData.timeline = timeline" type="range" min="3" max="120" step="1" required>
                            </div>
                            <div class="bot">
                                <p>3 Months</p>
                                <p>120 Months</p>
                            </div>
                        </div> 
                        <div class="salaryCard">
                            <div class="top">
                                <p>Total Savings</p>
                                <span class="value-display">{{ formatCurrency(income3) }}</span>
                            </div>
                            <div class="mid">
                                <input v-model.number="income3" @input="formData.total_savings = income3" type="range" min="5000" max="500000" step="1000" required>
                            </div>
                            <div class="bot">
                                <p>$5,000</p>
                                <p>Current savings across all accounts</p>
                                <p>$100,000</p>
                            </div>
                        </div>
                        <div class="salaryCard">
                            <div class="top">
                                <p>Emergency Fund</p>
                                <span class="value-display">{{ formatCurrency(income4) }}</span>
                            </div>
                            <div class="mid">
                                <input v-model.number="income4" @input="formData.emergency_fund = income4" type="range" min="5000" max="100000" step="1000" required>
                            </div>
                            <div class="bot">
                                <p>$5,000</p>
                                <p>Your Emergecny fund goal</p>
                                <p>$100,000</p>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            <div class="reviews">
                <h1>Specific numbers.</h1>
                <h2>Actual people</h2>
                <div class="cardsContainer" ref="tableRowRef" :class="{'animate-trigger2' : isTableRowIntersecting}">
                    <div class="revCard1">
                        <h3>$14,400 saved in 18 months</h3>
                        <span>John T. <span class="disc">— Software Engineer, Chicago</span></span>
                        <p class="bordbot">Started with $0 emergency fund. Automated $800/month into a HYSA. Hit 6-month runway by month 14 — four months ahead of projection.</p>
                        <div class="botCard">
                            <div class="botleft">
                                <p class="semi">$800</p>
                                <p class="miniText">Monthly auto-transfer</p>
                            </div>
                            <div class="botright">
                                <p class="semiGreen">-4 months</p>
                                <p class="miniText">vs plan</p>
                            </div>
                        </div>
                    </div>
                    <div class="revCard2">
                        <h3>$47,200 toward $60k target</h3>
                        <span>Priya & Daniel K. <span class="disc"> — Dual-income couple, Austin</span></span>
                        <p class="bordbot">Two accounts, one goal. Used sinking fund rules to coordinate contributions. Currently 78.7% to target — on track for Q3 2026 close.</p>
                        <div class="botCard">
                            <div class="botleft">
                                <p class="semi">$2,100</p>
                                <p class="miniText">Combined monthly</p>
                            </div>
                            <div class="botright">
                                <p class="semi">Aug 2026</p>
                                <p class="miniText">completion</p>
                            </div>
                        </div>
                    </div>
                    <div class="revCard3">
                        <h3>$8,900 in Year 1 of 529 plan</h3>
                        <span>Sarah O. <span class="disc">— Marketing Director, Seattle</span></span>
                        <p class="bordbot">Opened a 529 the month her daughter was born. Conservative strategy at 12% savings rate. Projected balance at age 18: $312,000 with 7% market return.</p>
                        <div class="botCard">
                            <div class="botleft">
                                <p class="semi">$740</p>
                                <p class="miniText">Monthly contribution</p>
                            </div>
                            <div class="botright">
                                <p class="semi">$312k</p>
                                <p class="miniText">Projected at 18</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="finishContainer">
                    <button @click="submitData" type="submit" class="finish">Sign Up !</button>
                </div>
            </div>
        </div>
</template>

<style>
    html {
        margin: 0;
        min-height: 100vh;
        background: #0f172a; 
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        background-attachment: fixed;
    }
</style>

<style scoped>
    @keyframes SideEnter {
        from {
            opacity: 0;
            transform: translateX(-800px);
        }

        to {
            opacity: 1;
            transform: translateX(0px);
        }
    }

    @keyframes fallIn {
        from {
            opacity: 0;
            transform: translateY(300px);
        }

        to {
            opacity: 1;
            transform: translateY(20px);
        }
    }

    * {
        margin: 0;
        padding: 0;
    }

    .titleContainer {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .Signup {
        display: grid;
        grid-template-columns: auto 1fr; 
        gap: 15px 20px; 
        max-width: 600px;
        margin: 20px auto;
        align-items: center; 
        padding: 20px;  
    }

    .countersContainer {
        display: flex;
        margin-bottom: -20px;
        flex-direction: column;
        width: 100%;
        margin-top: 170px;
        background-color: #1a1a2e;
        padding-top: 6rem;
        padding-bottom: 6rem; 
        background: 
        linear-gradient(to bottom, #22223d 0%, rgba(34, 34, 61, 0) 100%),
        linear-gradient(rgba(26, 26, 46, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(26, 26, 46, 0.04) 1px, transparent 1px),
        #F4F5F7;
        background-size: 
        100% 150px,   
        48px 48px,    
        48px 48px,    
        100% 100%;
        background-repeat: no-repeat, repeat, repeat, no-repeat;
        position: relative;
        z-index: 1;
        height: 50vh;
    }

    .countersContainer h2 {
        font-size: 4vw;
        font-family: DM Sans, sans-serif;
        color: rgb(26, 26, 46);
        line-height: 1.25;
        font-weight: 700;
        z-index: 10;
        margin-bottom: 5px;
        margin-left: 20px;
    }

    .adj {
        font-size: 1.125rem;
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        line-height: 1.75rem;
        z-index: 11;
        margin-bottom: -230px;
        margin-left: 30px;
    }

    .salaryCard {
        min-height: 11vh;
        height: 12vh;
        max-height: 13vh;
        background: rgba(255, 255, 255, 1);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        box-sizing: border-box;
    }

    .counters {
        display: grid;
        grid-template-columns: repeat(6, 1fr); 
        gap: 20px;
        width: 100%;
        max-width: 1200px; 
        margin: 0 auto;
        padding-top: 18rem;
        padding-bottom: 6rem; 
        position: relative;
        z-index: 1;
        opacity: 0;
        box-sizing: border-box;
    }

    .counters .salaryCard:nth-child(1),
    .counters .salaryCard:nth-child(2),
    .counters .salaryCard:nth-child(3) {
        grid-column: span 2;
    }

    .counters .salaryCard:nth-child(4),
    .counters .salaryCard:nth-child(5) {
        grid-column: span 3;
    }
    
    .top {
        display: flex;
        justify-content: space-around;
        flex-direction: row;
        gap: 20px;
        padding-top: 10px;
        width: 100%;
    }

    .status-msg {
        margin: 15px 0;
        padding: 12px;
        border-radius: 6px;
        font-size: 0.9rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: rgba(255, 255, 255, 0.05);
        color: #A3A3B5;
        text-align: center;
    }
    
    /* Switches background and text color to red if it detects an error phrase */
    .status-msg.error-msg {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .mid {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }

    .mid input {
        appearance: none;
        cursor: pointer;
        width: 60%;
        height: 3px;
        background: #2a2a45;
        outline: none;
        padding: 0px 0px 0px 0px;
        margin: 10px 0 10px;
    }

    .bot {
        display: flex;
        justify-content: space-around;
        align-items: center;
        flex-direction: row;
        gap: 20px;
        width: 100%;
        padding-bottom: 10px;
    }

    .bot p {
        font-family: JetBrains Mono, monospace;
        font-size: 10px;
        color: rgb(163, 163, 181);
    }

    .top span {
        font-family: JetBrains mono, monospace;
        color: rgba(26 26 46 1);
        font-weight: 600;
        font-size: 1.125rem;
        line-height: 1.75rem;
    }

    .top p {
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        letter-spacing: .1em;
        text-transform: uppercase;
        font-size: .75rem;
        line-height: 1rem;
    }

    .personal {
        display: flex;
        justify-content: center;
        align-items: center; 
        flex-direction: column;
        min-height: 100%;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .topRow {
        display: flex;
        justify-content: center;
        align-items: center; 
        flex-direction: column;
        overflow: hidden;
        margin-top: 10px;
        width: 60%;
        min-height: 97vh;
        background: rgb(34 34 61);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        gap: 40px;
    }

    .para {
        display: flex;
        flex-direction: column;
        gap: 45px;
    }

    .inputs {
        display: flex; 
        flex-direction: column;
        gap: 20px;
        margin-left: 20px;
    }

    .feat span {
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        line-height: 1.375;
        font-size: .875rem;
    }

    .form-content {
        display: flex;
        flex-direction: row; 
        align-items: flex-start;
    }

    .feat {
        display: grid;
        grid-template-columns: repeat(2, auto); 
        grid-auto-flow: column; 
        grid-template-rows: repeat(2, auto);
        gap: 20px 60px;
        margin: 0 auto 20px;
    }

    .form-content {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }

    .feat-item {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .feat-item svg {
        background: rgba(0, 200, 83, 0.4);
        padding: 6px;
        border-radius: 8px;
        width: 28px;
        height: 28px;
        flex-shrink: 0;
        color: rgb(0, 200, 83)
    }

    .feat span {
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        font-size: .875rem;
        white-space: nowrap;
    }

    .icon-box {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        background: rgba(0, 200, 83, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .reviews {
        /* display: flex; */
        height: auto; 
        min-height: 90vh;
        width: 100%;
        background-image: 
            linear-gradient(rgba(26, 26, 46, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(26, 26, 46, 0.04) 1px, transparent 1px);
        background-color: #F4F5F7;
        background-size: 48px 48px;
        background-repeat: repeat;
        margin-top: 0; 
        padding-top: 7px; 
        position: relative;
        clear: both;
    }
    
    .reviews h1 {
        font-size: 4vw;
        font-family: DM Sans, sans-serif;
        color: rgba(26, 26, 46, 1);
        line-height: 1.25;
        font-weight: 700;
        margin-left: 15px;
    }
    
    .reviews h2 {
        font-size: 4vw;
        font-family: DM Sans, sans-serif;
        color: rgba(163, 163, 181, 1);
        line-height: 1.25;
        font-weight: 700;
        margin-left: 15px;
    }
    
    .cardsContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        opacity: 0;
    }
    
    .revCard1, .revCard2, .revCard3 {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-direction: column;
        background-color: rgba(255, 255, 255, 1);
        margin: 10px;
        width: 31%;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        height: 50vh;
        margin: 30px 20px 0 0;
        transition: 350ms ease-in-out;
    }
    
    .revCard1 {
        border-top: #00C853 4px solid;
    }
    
    .revCard1 h3, .revCard2 h3, .revCard3 h3 {
        padding: 15px 0 0 10px;
        color: #1a1a2e;
        font-family: JetBrains Mono, monospace;
        line-height: 1;
        font-weight: 700;
        font-size: 1.875rem;
    }
    
    .revCard1 h3 {
        color: #00C853;
    }
    
    .revCard1 span, .revCard2 span, .revCard3 span {
        font-family: DM Sans, sans-serif;
        color: rgb(26, 26, 46);
        font-weight: 600;
        font-size: .875rem;
        line-height: 1.25rem;
        padding-left: 10px;
    }
    .revCard1 span:only-child, .revCard2 span:only-child, .revCard3 span:only-child {
        color: rgb(163, 163, 181);
        font-size: .75rem;
        line-height: 1rem;
        font-family: Manrope, sans-serif;
    }
    
    .revCard2:hover, .revCard3:hover {
        border: #00C853 1px solid;
    }
    
    .bordbot{
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        line-height: 1.625;
        font-size: .875rem;
        padding-left: 7px;
        padding-right: 5px;
        padding-bottom: 11%;
        /* border-bottom: 1px solid rgba(26, 26, 46, 0.08); */
    }
    
    .miniText {
        font-family: Manrope, sans-serif;
        color: rgb(163, 163, 181);
        line-height: 1.625;
        font-size: .875rem;
        padding-left: 7px;
        padding-right: 5px;
    }
    
    .botCard {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        gap: 200px;
    }
    
    .botleft {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-direction: column;
    }
    
    .semi {
        color: black;
        font-family: JetBrains Mono, monospace;
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.5rem;
    }
    
    .semiGreen {
        color: #00C853;
        font-family: JetBrains Mono, monospace;
        font-weight: 600;
        font-size: 1rem;
        line-height: 1.5rem;
    }
    
    p {
        color: #f0f0f0;
    }
    
    h1{
        color: #f0f0f0;
    }
    
    label {
        color: rgb(163 163 181);
        font-family: JetBrains Mono, monospace;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-size: 14px;
    }
    
    input {
        border-radius: .75rem;
        padding: 10px 20px;
        text-decoration: none;
        box-shadow: inset 2px 2px 5px rgba(0,0,0,0.1);
        font-family: Manrope, sans-serif;
        color: rgb(255, 255, 255);
        background-color: rgba(26, 26, 46, 1);
        font-size: .875rem;
        line-height: 1.25rem;
        border-color: rgba(163, 163, 181, .2);
        border-width: 1px;
    }
    
    button {
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
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        transform: translateY(3px);
        /* animation: fallIn 2s ease-in-out forwards; */
    }
    
    button:hover{
        transform: translateY(-10px);
        box-shadow: rgba(99, 102, 241, 0.4) 0px 10px 40px;
    }
    
    .finishContainer {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #F4F5F7;
        background-image: 
            linear-gradient(rgba(26, 26, 46, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(26, 26, 46, 0.04) 1px, transparent 1px);
        overflow: hidden;
        background-size: 48px 48px;
        background-repeat: repeat;
        margin-top: 89px;
        margin-bottom: 20px;
        height: 9vh;
        padding: 0;
    }

    .finish {
        background-color: #00C853;
        font-family: DM Sans, sans-serif;
        font-size: .875rem;
        line-height: 1.25rem;
    }

    .finish:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 32px rgba(0, 200, 83, .25);
    }

    .animate-trigger {
        opacity: 1;
        transform: translateX(0);
    }

    .animate-trigger2 {
        opacity: 1;
        transform: translateX(0);
    }

    .animate-trigger { animation: SideEnter 1.9s ease-in-out forwards;}
    .animate-trigger2 { animation: fallIn 1.55s ease-in-out forwards;}

    @media screen and (max-width: 1024px) {
    .topRow {
        width: 85%;
        padding: 40px 20px;
        min-height: auto;
    }

    .feat {
        grid-template-columns: 1fr;
        grid-auto-flow: row;
        grid-template-rows: auto;
        gap: 15px;
    }

    .countersContainer {
        height: auto;
        padding-top: 4rem;
        padding-bottom: 4rem;
    }

    .counters {
        grid-template-columns: repeat(2, 1fr) !important;
        padding-top: 14rem;
        padding-left: 20px;
        padding-right: 20px;
    }

    .counters .salaryCard:nth-child(1),
    .counters .salaryCard:nth-child(2),
    .counters .salaryCard:nth-child(3),
    .counters .salaryCard:nth-child(4),
    .counters .salaryCard:nth-child(5) {
        grid-column: span 2 !important;
    }

    .cardsContainer {
        flex-direction: column;
        align-items: center;
        padding: 0 20px;
    }

    .revCard1, .revCard2, .revCard3 {
        width: 100%;
        height: auto;
        margin: 15px 0;
    }

    .botCard {
        gap: 0;
        width: 100%;
        padding: 15px 10px;
        box-sizing: border-box;
    }
}

/* Mobile Devices (Max-width: 768px) */
@media screen and (max-width: 768px) {
    .topRow {
        width: 92%;
        gap: 25px;
    }

    .countersContainer h2,
    .reviews h1,
    .reviews h2 {
        font-size: 1.8rem;
        margin-left: 15px;
    }

    .adj {
        margin-bottom: -200px;
        font-size: 1rem;
    }

    .form-content {
        gap: 15px;
    }

    .para {
        gap: 38px;
    }

    .para label {
        font-size: 11px;
        height: 20px;
        display: flex;
        align-items: center;
    }

    .inputs {
        gap: 16px;
        margin-left: 10px;
    }

    .inputs input {
        height: 20px;
        padding: 5px 12px;
        font-size: 13px;
        width: 100%;
        box-sizing: border-box;
    }

    .counters {
        grid-template-columns: 1fr !important;
        padding-top: 15rem;
    }

    .counters .salaryCard:nth-child(1),
    .counters .salaryCard:nth-child(2),
    .counters .salaryCard:nth-child(3),
    .counters .salaryCard:nth-child(4),
    .counters .salaryCard:nth-child(5) {
        grid-column: span 1 !important;
    }

    .salaryCard {
        height: auto;
        padding: 15px 0;
    }

    .mid input {
        width: 80%;
    }

    .bot {
        flex-wrap: wrap;
        justify-content: center;
        text-align: center;
        gap: 5px 15px;
        padding: 0 10px;
    }

    /* Disable extreme horizontal animations on mobile to avoid layout clipping layout breaks */
    @keyframes SideEnter {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
}

/* Tiny Screens (Max-width: 480px) */
@media screen and (max-width: 480px) {
    .form-content {
        flex-direction: column;
        align-items: stretch;
        width: 100%;
        padding: 0 15px;
        box-sizing: border-box;
    }

    .para {
        flex-direction: row;
        flex-wrap: wrap;
        display: none; /* Simplifies layout on modern compact form patterns */
    }

    /* Converts form fields to stack neatly vertically */
    form {
        width: 100%;
    }

    .inputs {
        margin-left: 0;
        width: 100%;
    }

    .inputs input {
        width: 100%;
    }
    
    /* Dynamic placeholders act as labels if standard block layout collapses */
    .inputs input::placeholder {
        color: rgba(163, 163, 181, 0.7);
    }

    .finishContainer {
        margin-top: 40px;
    }
}
</style>