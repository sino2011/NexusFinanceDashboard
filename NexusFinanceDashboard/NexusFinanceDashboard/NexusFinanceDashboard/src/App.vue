<script setup>
    import { RouterView } from "vue-router";
    import SideBar from './views/SideBar.vue';
    import TopRow from "./views/TopRow.vue";
    import { ref } from "vue";
</script>

<template>
    <SideBar />
    <RouterView />
</template>

<style scoped></style>
