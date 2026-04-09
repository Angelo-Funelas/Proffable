<script setup>
    import { ref, onMounted } from 'vue';
    import api from "@/api/axios"

    const isModerator = ref(false);
    const domains = ref([]);

    onMounted(() => {
        fetchUser();
        fetchDomains();
    })
    const fetchUser = async () => {
        try {
            const res = await api.get("me/")
            console.log(res.data)
            isModerator.value = res.data.is_moderator;
        } catch(err) {
            console.error(err)
        }
    }

    async function fetchDomains(){
        try {
            const response = await api.get('institution-domains/')
            domains.value = response.data
            console.log(response.data)
        } catch(error){
            console.log("Error with fetching domains: ", error)
        }
    }

    async function createDomain() {
        try {
            await api.post('reviews/', {
                professor: route.params.professorId,
                review_rating: form.value.review_rating,
                comment_text: form.value.comment_text,
                received_grade: form.value.received_grade,
                tags: form.value.tags
            })
            message.value = 'Review submitted successfully!'
            isError.value = false
            form.value = { review_rating: '', comment_text: '', received_grade: '' }
        } catch (err) {
        const data = err.response?.data
        if (data?.non_field_errors || data?.detail) {
            message.value = data.non_field_errors?.[0] || data.detail
        } else {
            message.value = 'You have already reviewed this professor.'
        }
        isError.value = true
        }
    }
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
                <ul class="m-2">
                    <li v-for="domain in domains" class="my-1">
                        <div class="grid bg-gray-200 p-2 grid-cols-[80%_20%] grid-rows-1">
                            <span class="flex justify-start">{{ domain.domain }}</span>
                            <span class="flex justify-end"><img src="../assets/delete.svg" class="h-[24px]"></span>
                        </div>
                    </li>
                </ul>
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