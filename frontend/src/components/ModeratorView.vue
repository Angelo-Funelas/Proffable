<script setup>
    import Navbar from './Navbar.vue'
    import ReviewReport from "./ReviewReport.vue";
    import InstDomain from './InstDomain.vue';
    import { ref, onMounted } from 'vue';
    import api from "@/api/axios"

    const isModerator = ref(false);
    const reports = ref([]);
    const domains = ref([]);
    const me = ref({});

    onMounted(() => {
        fetchUser();
        fetchReports();
        fetchDomains();
    })
    const fetchUser = async () => {
        try {
            const res = await api.get("me/");
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
        } catch(error){
            console.log("Error with fetching domains: ", error)
        }
    }

    const domain = ref("");
    async function createDomain() {
        if (!domain.value) return;
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
        } catch(error){
            console.log("Error with fetching reports: ", error)
        }
    }
</script>
<template>
    <div class="min-h-screen flex flex-col bg-surface font-sans overflow-x-hidden">
        <Navbar/>
        
        <div v-if="isModerator" class="flex-grow p-6 md:p-12 max-w-7xl mx-auto w-full">
            
            <div class="mb-10 text-left">
                <h1 class="text-5xl font-bold text-text-main tracking-tight">
                    Moderator Dashboard<span class="text-primary">.</span>
                </h1>
                <p class="text-text-muted mt-2 text-lg">
                    Managing reports and domains for <span class="font-bold text-primary">{{ me.institution || 'your institution' }}</span>.
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                
                <div class="bg-card p-8 rounded-[24px] shadow-xl border border-gray-100 h-[650px] flex flex-col">
                    <div class="mb-6 text-left">
                        <h2 class="text-2xl font-bold text-text-main flex items-center gap-2">
                            Reports
                        </h2>
                        <p class="text-sm text-text-muted mt-1">Review and resolve reported content.</p>
                    </div>
                    
                    <div class="flex-grow overflow-y-auto pr-2 custom-scrollbar">
                        <p v-if="reports.length === 0" class="text-center py-10 text-text-muted italic">
                            No pending reports to review.
                        </p>
                        <ul class="space-y-4">
                            <li v-for="report in reports" :key="report.report_id">
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
                </div>

                <div class="bg-card p-8 rounded-[24px] shadow-xl border border-gray-100 h-[650px] flex flex-col">
                    <div class="mb-6 text-left">
                        <h2 class="text-2xl font-bold text-text-main flex items-center gap-2">
                            Email Domains
                        </h2>
                        <p class="text-sm text-text-muted mt-1">Whitelist domains for student verification.</p>
                    </div>

                    <form @submit.prevent="createDomain" class="flex gap-2 mb-6">
                        <input 
                            v-model="domain"
                            placeholder="e.g. student.ateneo.edu" 
                            class="flex-grow bg-surface border border-gray-100 rounded-xl px-4 py-3 text-sm text-text-main outline-none focus:border-primary/50 transition-all placeholder:text-text-muted/40"
                        >
                        <button class="bg-primary text-white px-6 py-3 rounded-xl font-bold text-sm shadow-md hover:brightness-110 active:scale-95 transition-all cursor-pointer">
                            Add
                        </button>
                    </form>

                    <div class="flex-grow overflow-y-auto pr-2 custom-scrollbar">
                        <ul class="space-y-2">
                            <li v-for="domainItem in domains" :key="domainItem.id">
                                <InstDomain
                                    @delete="fetchDomains"
                                    :domain="domainItem.domain"
                                    :id="domainItem.id"
                                />
                            </li>
                        </ul>
                    </div>
                </div>

            </div>
        </div>

        <div v-else class="flex-grow flex flex-col items-center justify-center p-6">
            <div class="bg-card p-10 rounded-[24px] shadow-xl border border-gray-100 text-center max-w-md">
                <div class="text-5xl mb-4">🚫</div>
                <h1 class="text-3xl font-bold text-text-main">Access Denied</h1>
                <p class="text-text-muted mt-2">This dashboard is reserved for Proffable moderators only.</p>
                <button 
                    @click="$router.push('/')" 
                    class="mt-8 w-full bg-primary text-white py-3 rounded-full font-bold cursor-pointer hover:brightness-110 transition-all active:scale-95 shadow-lg"
                >
                    Return to Homepage
                </button>
            </div>
        </div>
    </div>
</template>
<style scoped>
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #e5e7eb;
    border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #d1d5db;
}
</style>