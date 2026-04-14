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
const coursesTaught = ref([
  { code: '', name: '' }
]);

const removeCourse = (index) => {
  if (coursesTaught.value.length > 1) {
    coursesTaught.value.splice(index, 1);
  } else {
    coursesTaught.value[0].code = '';
    coursesTaught.value[0].name = '';
  }
};

const f_name = ref();
const m_name = ref();
const l_name = ref();
const email = ref();

const createProf = async () => {

  try {
    const response = await api.post("create-professor/", {
      f_name: f_name.value,
      m_name: m_name.value,
      l_name: l_name.value,
      email: email.value,
      courses: coursesTaught.value
    })

    alert("Form submitted.")

    f_name.value = ""
    m_name.value = ""
    l_name.value = ""
    email.value = ""
    for (const course of coursesTaught.value) {
      course.code = ""
      course.name = ""
    }

  } catch (error) {
    console.error(error)
    alert("Error submitting form.")
  }

}

const submitForm = async () => {
  document.getElementById("prof-form-submit").click()
}
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

    <button  @click="isModalOpen = true" class="bg-accent hover:bg-accent-hover text-white rounded-full px-[18px] py-1 w-max justify-center mx-auto cursor-pointer">
      Add a Professor
    </button>
    <BaseModal 
      :show="isModalOpen" 
      title="New Professor" 
      @close="isModalOpen = false"
    >
      <form @submit.prevent="createProf">
        <p class="text-text-muted mb-4">Can't find your professor? Create a new profile for them and wait for other students to leave their ratings & reviews.</p>
        <input v-model="f_name" type="text" placeholder="First Name" class="border border-primary p-2 w-full mb-3 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
        <input v-model="m_name" type="text" placeholder="Middle Name" class="border border-primary p-2 w-full mb-3 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
        <input v-model="l_name" type="text" placeholder="Last Name" class="border border-primary p-2 w-full mb-3 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
        <input v-model="email" type="email" placeholder="Email" class="border border-primary p-2 w-full mb-3 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
        <p class="inline-block">Courses Taught ({{ coursesTaught.length }})</p>
        <p
          @click="coursesTaught.push({code: '', name: ''})" 
          class="inline-block px-2  rounded-2xl mx-2 border border-primary text-primary text-sm hover:text-white hover:bg-primary cursor-pointer">Add +</p>
        <div v-for="(course, index) in coursesTaught" class="bg-surface p-2 rounded-lg m-2 grid grid-cols-[30%_60%_10%] items-center box-border">
          <input type="text" v-model="course.code" placeholder="Course Code" class="bg-white border border-primary p-2 mx-1 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
          <input type="text" v-model="course.name" placeholder="Course Name" class="bg-white border border-primary p-2 mx-1 rounded-lg text-sm text-text-main outline-none focus:border-[#5c898d]" required>
          <img
            v-if="index !== 0"
            @click="removeCourse(index)"
            src="../assets/delete.svg"
            class="h-6 justify-self-center cursor-pointer">
        </div>
        <input id="prof-form-submit" type="submit" class="hidden">
      </form>
    

        <template #footer>
          <div class="flex justify-end gap-2">
            <button @click="isModalOpen = false" class="cursor-pointer border border-primary text-[#719294] px-4 py-1.5 rounded-full text-sm hover:bg-[#e9e9e9] transition-colors">
                Cancel
            </button>
            <button @click="submitForm" class="cursor-pointer bg-primary text-white px-4 py-1.5 rounded-full text-sm hover:brightness-110 transition-all">
                Submit
            </button>
          </div>
        </template>
    </BaseModal>
  </div>
</template>