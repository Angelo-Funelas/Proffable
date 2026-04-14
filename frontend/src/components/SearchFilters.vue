<script setup>
import { ref, watch, onMounted } from 'vue'
import api from "@/api/axios"
import { useRouter, useRoute } from 'vue-router'
import RatingSelector from './RatingSelector.vue'
import BaseModal from './BaseModal.vue';

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

const isModalOpen = ref(false);
</script>

<template> 
  <div class="flex flex-col gap-2 text-left">
    <input 
      v-model="localQuery"
      @input="handleInput"
      class="rounded-2xl bg-card shadow-lg mt-[5px] h-[35px] px-3 text-text-main"
      placeholder="Search for a professor or course"
    />

    <div class="bg-card shadow-lg rounded-xl p-[18px] flex flex-col gap-2 text-left">
      <div class="relative">
        <select 
          v-model="selectedInstitution" 
          @change="updateURL" 
          class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] appearance-none outline-none"
        >
          <option value="">University</option>
          <option v-for="inst in institutions" :key="inst.institution_id" :value="inst.name">{{ inst.name }}</option>
        </select>
        <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
      </div>
              
      <div class="relative">
        <select 
          v-model="selectedCourse" 
          @change="updateURL" 
          class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] appearance-none outline-none"
        >
          <option value="">Course</option>
          <option v-for="c in courses" :key="c.course_id" :value="c.course_code">{{ c.course_code }}</option>
        </select>
        <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
      </div>
      <div class="text-center">
        <RatingSelector :initialRating="rating_query" @rate="updateStarQuery"/>
        <p class="text-center text-text-muted">Average Rating</p>
      </div>
    </div>

    <button  @click="isModalOpen = true" class="bg-accent text-white rounded-full px-[18px] py-1 w-max justify-center mx-auto">
      Add a Professor
    </button>
    <BaseModal 
      :show="isModalOpen" 
      title="New Professor" 
      @close="isModalOpen = false"
    >
      <template #footer>
        <button @click="isModalOpen = false">Confirm</button>
      </template>
    </BaseModal>
  </div>
</template>