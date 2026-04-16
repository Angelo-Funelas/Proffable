<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from "@/api/axios"
import RatingSelector from './RatingSelector.vue'

const props = defineProps({
  reviewId: Number,
  editing: Boolean,
  review_rating: Number,
  grade_received: String,
  comment_text: String,
  course: String,
  semester_term: String,
  semester_year: String,
  tags:Array
})

const route = useRoute()
const message = ref('')
const isError = ref(false)
const tags = ref([])

const courses = ref([])

const SEMESTER_TERMS = [
  { value: '1st', label: '1st Semester' },
  { value: '2nd', label: '2nd Semester' },
  { value: 'summer', label: 'Summer' },
]

const emit = defineEmits(['submitReview', 'cancelReview']);

const form = ref({
  review_rating: props.review_rating,
  comment_text: props.comment_text,
  received_grade: props.grade_received,
  tags: [],
  course: '',           
  semester_term: '',      
  semester_year: '',      
})
const handleRate = (value) => {
  form.value.review_rating = value;
};

onMounted(async () => {
  try {
    const [tagRes, courseRes] = await Promise.all([
      api.get('tags/'),
      api.get(`professors/${route.params.professorId}/courses/`),
    ])
    tags.value = tagRes.data
    courses.value= courseRes.data
    console.log("hi")
    if (props.editing && props.tags) {
      form.value.tags = props.tags.map(t => t.tag_id)
      form.value.course = courseRes.data.find(
        c => c.course_code = props.course
      )?.course_id || ''
      form.value.semester_term = SEMESTER_TERMS.find(
        s => s.label === props.semester_term
      )?.value || ''

      form.value.semester_year = props.semester_year
    }
    console.log(props)
    console.log(form.value)
  } catch (err) {
    console.error("Failed to load tags data", err)
  }
  
})

const toLetterGrade = (input) => {
  const n = parseFloat(input)
  if (isNaN(n)) return input
  if (n >= 90) return 'A'
  if (n >= 80) return 'B'
  if (n >= 70) return 'C'
  if (n >= 60) return 'D'
  return 'F'
}

function jsonPrintHelper(string){
  return string
  .replace(/_/g, ' ') 
  .replace(/\b\w/g, char => char.toUpperCase());
}

// Call Backend for Review
async function submitReview() {
  const normalizedGrade = toLetterGrade(form.value.received_grade)
  try {
    if (props.editing) {
      await api.put(`reviews/${props.reviewId}/`, {
        professor: route.params.professorId,
        review_rating: form.value.review_rating,
        comment_text: form.value.comment_text,
        received_grade: normalizedGrade,
        tags: form.value.tags,
        course: form.value.course,
        semester_term: form.value.semester_term,
        semester_year: form.value.semester_year,
      })
      message.value = 'Edited Review!'
    } else {
      await api.post('reviews/', {
        professor: route.params.professorId,
        review_rating: form.value.review_rating,
        comment_text: form.value.comment_text,
        received_grade: normalizedGrade,
        tags: form.value.tags,
        course: form.value.course,            
        semester_term: form.value.semester_term,  
        semester_year: form.value.semester_year,  
      })
      message.value = 'Submitted Review!'
    }
    isError.value = false
    emit('submitReview', form.value.review_rating, form.value.received_grade, form.value.comment_text)
    form.value = { 
      review_rating: '', 
      comment_text: '', 
      received_grade: '', 
      tags:[], 
      course: '',           
      semester_term: '',      
      semester_year: '',  }
  } catch (err) {
    const errors = err.response?.data

    if (errors) {
      message.value = Object.entries(errors)
        .map(([field, msgs]) => `${jsonPrintHelper(field)}: ${msgs.join("\n")}`)
        .join("\n")
    } else {
      message.value = "Something went wrong"
    }
  }
}



function toggleTag(id) {
  if (form.value.tags.includes(id)) {
    form.value.tags = form.value.tags.filter(x => x !== id)
  } else {
    form.value.tags.push(id)
  }
}

</script>

<template>
  <div>
    <form @submit.prevent="submitReview" class="space-y-4">
        <h1 class="text-2xl font-bold text-text-main text-left" v-if="!editing">Write a Review</h1>
        
        <div class="flex flex-col gap-1">
            <span class="text-sm font-bold text-text-main">Rating</span>
            <RatingSelector @rate="handleRate" :initialRating="form.review_rating"/>
        </div>

        <div class="flex flex-col gap-1">
          <span class="text-sm font-bold text-text-main">Course Details</span>
          <div class="flex gap-2">
            <select v-model="form.course" class="bg-surface border border-gray-200 rounded-xl my-2 p-2 text-text-main w-64 shadow-sm">
              <option disabled value="">Select a Course</option>
              <option v-for="c in courses" :key="c.course_id" :value="c.course_id">
                {{ c.course_code }}
              </option>
            </select>

            <select v-model="form.semester_term" class="bg-surface border border-gray-200 rounded-xl my-2 p-2 text-text-main w-64 shadow-sm">
              <option disabled value="">Select Semester</option>
              <option v-for="s in SEMESTER_TERMS" :key="s.value" :value="s.value">
                {{ s.label }}
              </option>
            </select>

            <input
              type="text"
              v-model="form.semester_year"
              class="bg-surface border border-gray-200 rounded-xl my-2 p-2 text-text-main w-64 shadow-sm"
              placeholder="Academic Year: e.g. 2024-2025"
              maxlength="9"
            />
          </div>
        </div>

        <div class="flex flex-col gap-1">
            <span class="text-sm font-bold text-text-main">Grade Received</span>
            <input 
                maxlength="12" 
                type="text" 
                v-model="form.received_grade" 
                class="bg-surface border border-gray-200 rounded-xl p-3 text-text-main w-full md:w-64 focus:border-primary outline-none transition-all shadow-sm" 
                placeholder="e.g. A, 95"
            >
        </div>

        <div class="flex flex-col gap-1">
            <span class="text-sm font-bold text-text-main">Your Experience</span>
            <textarea 
                v-model="form.comment_text" 
                rows="4"
                class="bg-surface border border-gray-200 rounded-xl resize-none w-full text-text-main p-3 focus:border-primary outline-none transition-all shadow-sm" 
                placeholder="What was good? What could be improved?"
            ></textarea>
        </div>

        <div class="space-y-2">
            <h1 class="text-sm font-bold text-text-main">Select Tags:</h1>
            <div class="flex flex-wrap gap-2">
                <div 
                    v-for="t in tags" 
                    :key="t.tag_id"
                    @click="toggleTag(t.tag_id)"
                    class="px-3 py-1.5 rounded-full cursor-pointer text-xs font-bold transition-all border"
                    :class="form.tags.includes(t.tag_id) 
                        ? 'bg-primary text-white border-primary shadow-md scale-105' 
                        : 'bg-surface text-text-muted border-gray-200 hover:border-primary hover:text-primary'"
                >
                    {{ t.tag_name }}
                </div>
            </div>
        </div>

        <div class="flex gap-2 pt-2">
            <button type="submit" class="bg-accent hover:brightness-110 text-white rounded-full px-6 py-2 font-bold transition-all shadow-md cursor-pointer">
                <span v-if="!editing">Submit Review</span>  
                <span v-if="editing">Save Changes</span>  
            </button>
            
            <button v-if="editing" @click="$emit('cancelReview')" type="button" class="bg-surface text-text-muted border border-gray-200 rounded-full px-6 py-2 font-bold hover:bg-gray-100 transition-all cursor-pointer">
                Cancel
            </button>
        </div>

        <p v-if="message" class="text-sm font-medium animate-pulse" :class="isError ? 'text-red-500' : 'text-green-600'">
            {{ message }}
        </p>
    </form>
    </div>
</template>