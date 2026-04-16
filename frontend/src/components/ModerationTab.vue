<script setup>
import { ref, onMounted } from 'vue'
import api from "@/api/axios"
import ReviewReport from "./ReviewReport.vue"
import InstDomain from './InstDomain.vue'

const props = defineProps({
  profile: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['message'])

const reports = ref([])
const domains = ref([])
const domain = ref("")

onMounted(() => {
  fetchReports()
  fetchDomains()
})

async function fetchDomains() {
  try {
    const response = await api.get('institution-domains/')
    domains.value = response.data
  } catch (error) {
    console.log("Error with fetching domains: ", error)
    emit('message', { text: "Failed to load domains.", type: "error" })
  }
}

async function createDomain() {
  if (!domain.value) return
  try {
    await api.post('institution-domains/', { domain: domain.value })
    domain.value = ""
    fetchDomains()
    emit('message', { text: "Domain added.", type: "success" })
  } catch (err) {
    console.error(err)
    emit('message', { text: "Failed to add domain.", type: "error" })
  }
}

async function fetchReports() {
  try {
    const response = await api.get('review-reports/')
    reports.value = response.data
  } catch (error) {
    console.log("Error with fetching reports: ", error)
    emit('message', { text: "Failed to load reports.", type: "error" })
  }
}
</script>

<template>
  <div class="moderation-tab">
    <div class="mb-8 text-left">
      <h1 class="text-4xl font-bold text-text-main tracking-tight">
        Moderator Dashboard<span class="text-primary">.</span>
      </h1>
      <p class="text-text-muted mt-2 text-lg">
        Managing reports and domains for
        <span class="font-bold text-primary">{{ profile.institution || 'your institution' }}</span>.
      </p>
    </div>

    <div class="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
      <!-- Reports -->
      <div class="bg-card p-6 rounded-[24px] shadow-xl border border-gray-100 h-[600px] flex flex-col">
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

      <!-- Email Domains -->
      <div class="bg-card p-6 rounded-[24px] shadow-xl border border-gray-100 h-[600px] flex flex-col">
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
          <button
            class="bg-primary hover:bg-primary-hover text-white px-6 py-3 rounded-xl font-bold text-sm shadow-md active:scale-95 transition-all cursor-pointer border-0"
          >
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