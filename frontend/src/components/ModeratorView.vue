<script setup>
    import { ref, onMounted } from 'vue';
    const isModerator = ref(true);
</script>
<template>
    <div v-if="isModerator" class="h-screen py-10 mx-40">
        <h1>Moderator Dashboard</h1>
        <div class="moderator-dashbaord mt-5 grid grid-cols-[50%_50%] grid-rows-[50%_50%] h-full gap-4 text-black">
            <div class="row-span-2">
                <h2>Reports</h2>
                <p>Manage reported reviews.</p>
            </div>
            <div>
                <h2>Email Domains</h2>
                <p class="text-black">Manage known email domains used by students.</p>
                <form>
                    <input type="email" placeholder="e.g. student.ateneo.edu" class="outline-1 px-2">
                    <button class="mx-2 bg-[#d2d2d2] px-2">Add Domain</button>
                </form>
            </div>
            <div>
                <h2>Professor Profiles</h2>
                <p>Merge, Delete, and Modify Professor Profiles.</p>
            </div>
        </div>
        </div>
    <div v-else>
        <h1>You do not have permission.</h1>
    </div>
</template>
<style scoped>
    @import "tailwindcss";
    h1 {
        @apply text-6xl font-bold text-left;
    }
    h2 {
        @apply text-4xl;
    }
    .moderator-dashbaord > div {
        @apply p-4 bg-white shadow-md rounded-2xl;
    }
</style>