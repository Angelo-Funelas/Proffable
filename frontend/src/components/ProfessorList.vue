<script setup>
import { ref, onMounted, watch } from 'vue'
import api from "@/api/axios"
import ProfCard from './ProfCard.vue'
import SearchFilters from './SearchFilters.vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from './Navbar.vue'

const professors = ref([])
const isLoading = ref(false)
const route = useRoute()
const router = useRouter()

async function fetchProfessors(filters = {}) {
    isLoading.value = true
    const params = {
        search: filters.q || route.query.q || '',
        institution: filters.institution || route.query.institution || '',
        course: filters.course || route.query.course || '',
        min_rating: filters.min_rating || route.query.min_rating || undefined
    }

    try {
        const response = await api.get('professors/', { params })
        professors.value = response.data
    } catch(error) {
        console.error("Fetch error:", error)
    } finally {
        isLoading.value = false
    }
}

watch(() => route.query, (newQuery) => {
    fetchProfessors(newQuery)
}, { immediate: true })

const goToProf = (professorId) => {
    router.push(`/professor/${professorId}`)
}
</script>

<template>
<div class="min-h-screen bg-surface flex flex-col overflow-x-hidden">
    <Navbar/>
    
    <main class="grid grid-cols-[4fr_11fr] gap-x-[30px] w-full p-[64px]"> 
        
        <aside>
            <SearchFilters />
        </aside>

        <section>
            <div class="mb-6">
                <h1 class="text-5xl font-bold text-left text-primary tracking-tight">Professors</h1>
                
                <p v-if="!isLoading" class="text-left mt-2 ml-1 text-text-muted font-medium">
                    <span v-if="professors.length > 0">
                        {{ professors.length }} results found 
                        <span v-if="route.query.q">for "{{ route.query.q }}"</span>
                    </span>
                    <span v-else>No results found for your search.</span>
                </p>
            </div>

            <div v-if="isLoading" class="flex justify-center py-20">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>

            <ul v-else class="grid grid-cols-1 gap-y-[12px]">
                <li v-for="prof in professors" :key="prof.professor_id" 
                    @click="goToProf(prof.professor_id)" 
                    class="cursor-pointer transition-all duration-200 hover:scale-[1.01] active:scale-[0.99] origin-left">
                    <ProfCard
                        :lname="prof.l_name"
                        :fname="prof.f_name"
                        :avgScore="prof.avg_rating || 0"
                        :numReviews="prof.review_count"
                        :favoriteCount="prof.favorite_count"
                        :is_favorited="prof.is_favorited"
                        :tags="prof.tags"
                        :institutions="prof.institutions"
                    />
                </li>
            </ul>
        </section>
    </main>
</div> 
</template>