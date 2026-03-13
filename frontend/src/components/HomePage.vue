<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from "@/api/axios"
import Navbar from './Navbar.vue';
import RatingSelector from './RatingSelector.vue';

const router = useRouter()
const searchQuery = ref('')
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

const handleSearch = () => {
  router.push({ 
    path: '/professors', 
    query: { q: searchQuery.value, institution: selectedInstitution.value, 
      course: selectedCourse.value, min_rating:rating.value|| undefined}
  })
}
const rating = ref(0);
const handleRate = (value) => {
  rating.value = value;
};
</script>

<template>
  <div class="main-container">
    <Navbar/>
    <div class="flex flex-col items-center mt-[80px]">
      <div class="flex flex-col items-center mb-[40px]">
        <div class="flex items-center">
          <img src="../assets/ProffableLogo.png" class="h-[150px]" />
          <span class="text-[#505946] text-[100px] font-bold mb-[5px] ml-[-15px]">roffable</span>
        </div>
        <p class="text-[#0B0D09] text-2xl font-bold italic -mt-10 -mr-20">Choosing a professor made Proffable.</p>
      </div>

      <div class="w-[720px] relative mb-[-30px] z-10">
        <div class="flex items-center bg-white rounded-full shadow-md px-[24px] py-[18px]">
          <input v-model="searchQuery" @keyup.enter="handleSearch" type="text" placeholder="Search for a professor or course" class="flex-1 outline-none text-lg text-[#719294]" />
          <button class="ml-[20px] font-medium text-[#0B0D09] flex items-center gap-[6px]">Filter <span>▾</span></button>
        </div>
      </div>

      <div class="w-[720px] bg-[#5c898d] rounded-[18px] pt-[60px] pb-[30px] px-[40px] shadow-lg">

        <!-- DROPDOWNS -->
        <div class="flex gap-[20px] mb-[10px]">

          <div class="flex-1">
            <select v-model="selectedInstitution" class="w-full px-[18px] py-[14px] rounded-[14px] bg-gray-100 text-[#719294]">
              <option value="">University</option>
              <option v-for="inst in institutions" :key="inst.institution_id" :value="inst.name">{{ inst.name }}</option>
            </select>
          </div>
          <div class="flex-1">
            <select v-model="selectedCourse" class="w-full px-[18px] py-[14px] rounded-[14px] bg-gray-100 text-[#719294]">
              <option value="">Courses</option>
              <option v-for="c in courses" :key="c.course_id" :value="c.course_code">{{ c.course_code }}</option>
            </select>
          </div>

        </div>

        <RatingSelector @rate="handleRate"/>
        <p class="text-center text-white opacity-80">Average Rating</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
:global(#app) {
  max-width: none !important;
  width: 100vw !important;
  padding: 0 !important;
  margin: 0 !important;
}

:global(body) {
  margin: 0 !important;
  display: block !important;
}

.navbar {
  width: 100%;
  background-color: #5c898d;
  height: 4rem;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.logo-circle {
  background-color: #d9d9d9;
  border-radius: 9999px;
  height: 2.5rem;
  width: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo-img {
  height: 1.75rem;
  width: 1.75rem;
  object-fit: contain;
}

</style> 