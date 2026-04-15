<script setup>
import { ref, watch, onMounted } from 'vue'
import api from "@/api/axios"
import { useRouter, useRoute } from 'vue-router'
import RatingSelector from './RatingSelector.vue'

const router = useRouter()
const route = useRoute()

const rating_query = ref(route.query.min_rating || undefined)
const localQuery = ref(route.query.q || '')
const selectedInstitution = ref(route.query.institution || '')
const selectedCourse = ref(route.query.course || '')

let debounceTimer = null
const institutions = ref([])
const courses = ref([])

const updateURL = () =>{
  router.push({
    path: '/professors',
    query: {
      q: localQuery.value || undefined,
      institution: selectedInstitution.value || undefined,
      course: selectedCourse.value || undefined,
      min_rating: rating_query.value || undefined
    }
  })
}

const handleInput = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(updateURL, 500)
}

onMounted(async () => {
  try {
    const [instRes, courseRes] = await Promise.all([
      api.get('institutions/'),
      api.get('courses/')
    ])
    institutions.value = instRes.data
    courses.value = courseRes.data
  } catch (err) {
    console.error("Failed to load filter data", err)
  }
})

const updateStarQuery = (rating) => {
  rating_query.value = rating
  updateURL()
}

</script>

<template> 
  <div class="flex flex-col gap-3 text-left">
    <div class="relative">
      <input 
        v-model="localQuery"
        @input="handleInput"
        class="w-full rounded-2xl bg-card shadow-md border border-gray-100 h-[48px] px-5 pr-12 text-text-main outline-none focus:border-primary transition-all placeholder:opacity-50"
        placeholder="Search for a professor..."
      />
      <svg class="h-5 w-5 absolute right-4 top-1/2 -translate-y-1/2 text-primary opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <div class="bg-card shadow-md border border-gray-100 rounded-xl p-5 flex flex-col gap-4 text-left">
      
      <div class="relative">
        <select 
          v-model="selectedInstitution" 
          @change="updateURL" 
          class="w-full h-[45px] rounded-xl px-4 pr-10 bg-surface text-primary font-bold border border-transparent appearance-none outline-none focus:border-primary/20 cursor-pointer text-sm"
        >
          <option value="">University</option>
          <option v-for="inst in institutions" :key="inst.institution_id" :value="inst.name">
            {{ inst.name }}
          </option>
        </select>
        <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none opacity-50 text-primary text-xs">▼</div>
      </div>
              
      <div class="relative">
        <select 
          v-model="selectedCourse" 
          @change="updateURL" 
          class="w-full h-[45px] rounded-xl px-4 pr-10 bg-surface text-primary font-bold border border-transparent appearance-none outline-none focus:border-primary/20 cursor-pointer text-sm"
        >
          <option value="">Courses</option>
          <option v-for="c in courses" :key="c.course_id" :value="c.course_code">
            {{ c.course_code }}
          </option>
        </select>
        <div class="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none opacity-50 text-primary text-xs">▼</div>
      </div>

      <div class="pt-3 border-t border-gray-50 flex flex-col items-center">
        <RatingSelector :initialRating="Number(rating_query)" @rate="updateStarQuery"/>
        <p class="text-[10px] font-bold text-text-muted uppercase tracking-widest mt-2 opacity-60">Minimum Rating</p>
      </div>
    </div>

    <button class="bg-accent hover:brightness-110 text-white rounded-full px-6 py-3 w-full font-bold shadow-md transition-all text-sm mt-2 active:scale-95">
      + Add a Professor
    </button>
  </div>
</template>