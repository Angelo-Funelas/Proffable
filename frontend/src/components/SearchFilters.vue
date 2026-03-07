<script setup>
import { ref, onMounted } from 'vue'
import api from "@/api/axios"

const emit = defineEmits(['search'])

// Added state for filters
const localQuery = ref('')
const selectedInstitution = ref('')
const selectedCourse = ref('')

const institutions = ref([])
const courses = ref([])

onMounted(async () => {
  const [instRes, courseRes] = await Promise.all([
    api.get('institutions/'),
    api.get('courses/')
  ])
  institutions.value = instRes.data
  courses.value = courseRes.data
})

const triggerSearch = () => {
  emit('search', {
    q: localQuery.value,
    institution: selectedInstitution.value,
    course: selectedCourse.value
  })
}
</script>

<template> 
  <div class="flex flex-col gap-2 text-left">
    <input 
      v-model="localQuery"
      @input="triggerSearch"
      class="rounded-2xl bg-[#FFFFFF] form_text mt-[5px] h-[35px] px-3 text-[#719294] "
      placeholder="Search for a professor or course"
    />

    <div class="bg-[#52848A] rounded-xl p-[18px] flex flex-col gap-2 text-left">
      <div class="relative">
        <select v-model="selectedInstitution" @change="triggerSearch" class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] form_text appearance-none outline-none">
          <option value="">University</option>
          <option v-for="inst in institutions" :key="inst.institution_id" :value="inst.name">{{ inst.name }}</option>
        </select>
        <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
      </div>
      
      <div class="relative">
        <select v-model="selectedCourse" @change="triggerSearch" class="w-full h-[40px] rounded-2xl px-6 pr-12 bg-[#E9E9E9] form_text appearance-none outline-none">
          <option value="">Course</option>
          <option v-for="c in courses" :key="c.course_id" :value="c.course_code">{{ c.course_code }}</option>
        </select>
        <img src="../assets/DropdownArrow.svg" class="h-[5px] absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"/>
      </div>

      <div class="grid grid-cols-1 gap-1 justify-center">
        <div class="flex justify-center">
          <img src="../assets/BigStar.svg" class="h-[48px]" />
          <img src="../assets/BigStar.svg" class="h-[48px]" />
          <img src="../assets/BigStar.svg" class="h-[48px]" />
          <img src="../assets/BigStar.svg" class="h-[48px]" />
          <img src="../assets/BigStar.svg" class="h-[48px]" />
        </div>
        <p class="text-center">Average Rating</p>
      </div>
    </div>

    <button class="bg-[#52848A] rounded-full px-[18px] py-1 w-max justify-center mx-auto">
      Add a Professor
    </button>
  </div>
</template>