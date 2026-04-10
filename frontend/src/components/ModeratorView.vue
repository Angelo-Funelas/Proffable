<script setup>
    import Navbar from './Navbar.vue'
    import ReviewReport from "./ReviewReport.vue";
    import InstDomain from './InstDomain.vue';
    import { ref, onMounted } from 'vue';
    import api from "@/api/axios"

    const isModerator = ref(false);
    const reports = ref([]);
    const domains = ref([]);
    const me = ref();

    onMounted(() => {
        fetchUser();
        fetchReports();
        fetchDomains();
    })
    const fetchUser = async () => {
        try {
            const res = await api.get("me/");
            console.log(res.data);
            me.value = res.data;
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
    const domain = ref();
    async function createDomain() {
        try {
            await api.post('institution-domains/', {
                domain: domain.value
            })
            domain.value = ""
            fetchDomains();
        } catch (err) {
            console.error(err)
        }
    }

    async function fetchReports() {
        try {
            const response = await api.get('review-reports/')
            reports.value = response.data
            console.log(response.data)
        } catch(error){
            console.log("Error with fetching reports: ", error)
        }
    }
</script>
<template>
    <Navbar/>
    <div v-if="isModerator" class="h-screen py-10 mx-40 mb-10">
        <h1>Moderator Dashboard</h1>
        <p class="text-left">Managing reports, domains, and profiles for {{ me.institution }}.</p>
        <div class="moderator-dashbaord mt-5 grid grid-cols-[50%_50%] grid-rows-[50%_50%] h-full gap-4 text-black">
            <div class="row-span-2 overflow-hidden">
                <h2>📢Reports</h2>
                <p>Manage reported reviews.</p>
                <ul class="m-2 h-full overflow-y-auto">
                    <p v-if="reports.length === 0">No pending reports to review.</p>
                    <li v-for="report in reports" class="my-1">
                        <ReviewReport
                            @resolve="fetchReports"
                            :reportId="report.report_id"
                            :description="report.description"
                            :reason="report.reason"
                            :reporter="report.reporter_name"
                            :author="report.author"
                            :review_id="report.review"
                            :created_at="report.created_at"
                        />
                    </li>
                </ul>
            </div>
            <div class="row-span-2">
                <h2>📧Email Domains</h2>
                <p class="text-black">Manage known email domains used by students.</p>
                <form @submit.prevent="createDomain">
                    <input placeholder="e.g. student.ateneo.edu" v-model="domain" class="outline-1 px-2">
                    <button class="mx-2  px-2">Add Domain</button>
                </form>
                <ul class="m-2">
                    <li v-for="domain in domains" class="my-1">
                        <InstDomain
                            @delete="fetchDomains"
                            :domain="domain.domain"
                            :id="domain.id"
                        />
                    </li>
                </ul>
            </div>
            <!-- <div>
                <h2>👤Professor Profiles</h2>
                <p>Merge, Delete, and Modify Professor Profiles.</p>
            </div> -->
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
        @apply text-[30px];
    }
    .moderator-dashbaord > div {
        @apply p-4 bg-white shadow-md rounded-2xl;
    }
    p {
        @apply text-black;
    }
</style>