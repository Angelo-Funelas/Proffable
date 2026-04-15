<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from "@/api/axios"
import Navbar from './Navbar.vue';
import RatingSelector from './RatingSelector.vue';
import LogoIcon from './LogoIcon.vue';

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
  <Navbar/>
  <header class="pt-20 h-[80vh] ">
    <div class="flex flex-col items-center">
      
      <div class="flex flex-col items-center mb-[40px]">
        <div class="flex items-center">
          <LogoIcon class="h-40 mr-3"/>
          <span class="text-primary text-[100px] font-roboto mb-[5px] ml-[-15px]">roffable</span>
        </div>
        <p class="text-text-main text-2xl font-bold italic -mt-10 -mr-25">Choosing a professor made Proffable.</p>
      </div>

      <div class="w-[720px] relative mb-[-30px] z-10">
        <div class="flex items-center bg-white rounded-full shadow-lg px-[30px] py-[20px] border border-gray-100">
          <input 
            v-model="searchQuery" 
            @keyup.enter="handleSearch" 
            type="text" 
            placeholder="Search for a professor or course..." 
            class="flex-1 outline-none text-xl text-text-main placeholder:opacity-50" 
          />
          <svg @click="handleSearch" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary cursor-pointer hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <div class="w-[720px] bg-card rounded-[24px] pt-[70px] pb-[40px] px-[50px] shadow-xl border border-gray-50">

        <div class="flex gap-[20px] mb-[25px]">
          <div class="flex-1 relative">
            <select v-model="selectedInstitution" class="w-full px-[20px] py-[14px] rounded-[16px] bg-surface text-primary font-bold appearance-none outline-none border border-transparent focus:border-primary/20 cursor-pointer">
              <option value="">University</option>
              <option v-for="inst in institutions" :key="inst.institution_id" :value="inst.name">{{ inst.name }}</option>
            </select>
            <div class="absolute right-5 top-1/2 -translate-y-1/2 pointer-events-none opacity-50 text-primary">▾</div>
          </div>

          <div class="flex-1 relative">
            <select v-model="selectedCourse" class="w-full px-[20px] py-[14px] rounded-[16px] bg-surface text-primary font-bold appearance-none outline-none border border-transparent focus:border-primary/20 cursor-pointer">
              <option value="">Courses</option>
              <option v-for="c in courses" :key="c.course_id" :value="c.course_code">{{ c.course_code }}</option>
            </select>
            <div class="absolute right-5 top-1/2 -translate-y-1/2 pointer-events-none opacity-50 text-primary">▾</div>
          </div>
        </div>

        <div class="flex flex-col items-center gap-2">
            <RatingSelector :initialRating="rating" @rate="handleRate"/>
            <p class="text-xs font-bold uppercase tracking-widest text-text-muted opacity-60">Minimum Average Rating</p>
        </div>
      </div>
    </div>
    <div class=" opacity-30 grid grid-rows-1 grid-cols-29 items-end">
      <img src="/ateneo.png" class="row-1 col-start-1 col-span-8">
      <img src="/ust.png" class="row-1 col-start-8 col-span-8">
      <img src="/up.png" class="row-1 col-start-15 col-span-8">
      <img src="/dlsu.png" class="row-1 col-start-22 col-span-8">
    </div>
  </header>
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