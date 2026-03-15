<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import Navbar from './Navbar.vue';
import api from "@/api/axios"

const route = useRoute()
const message = ref('')
const isError = ref(false)

const form = ref({
  review_rating: '',
  comment_text: '',
  received_grade: ''
})

// Call Backend for Review 
async function submitReview() {
  try {
    await api.post('reviews/', {
      professor: route.params.professorId,
      review_rating: form.value.review_rating,
      comment_text: form.value.comment_text,
      received_grade: form.value.received_grade
    })
    message.value = 'Review submitted successfully!'
    isError.value = false
    form.value = { review_rating: '', comment_text: '', received_grade: '' }
  } catch (err) {
  const data = err.response?.data
  if (data?.non_field_errors || data?.detail) {
    message.value = data.non_field_errors?.[0] || data.detail
  } else {
    message.value = 'You have already reviewed this professor.'
  }
  isError.value = true
}
}
</script>

<template>
  <div class="min-h-screen bg-[#e9e9e9] flex flex-col">
    
    <Navbar/>
  
    <div class="flex-1 flex items-center justify-center px-4">
      <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 flex flex-col gap-6">
    
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-2xl font-bold">
          <span class="text-[#0B0D09]">Leave a </span>Review
        </h1>
        <p class="text-sm text-[#0B0D09] mt-1">
          Share your experience to help other students
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="submitReview" class="flex flex-col gap-5">

        <!-- Rating -->
        <div class="flex flex-col gap-1">
          <label class="text-sm text-[#719294]">Rating (1–5)</label>
          <div class="flex items-center border rounded-lg px-3 py-2 focus-within:border-[#719294]">
            <span class="mr-2">⭐</span>
            <input
              type="number"
              v-model="form.review_rating"
              min="1"
              max="5"
              required
              class="w-full outline-none text-[#719294]"
            />
          </div>
        </div>

        <!-- Grade -->
        <div class="flex flex-col gap-1">
          <label class="text-sm text-[#719294]">Grade Received</label>
          <div class="flex items-center border rounded-lg px-3 py-2 focus-within:border-[#719294]">
            <span class="mr-2">🎓</span>
            <input
              type="text"
              v-model="form.received_grade"
              placeholder="e.g. A+, B"
              class="w-full outline-none text-[#719294]"
            />
          </div>
        </div>

        <!-- Comment -->
        <div class="flex flex-col gap-1">
          <label class="text-sm text-[#719294]">Comment</label>
          <div class="flex border rounded-lg px-3 py-2 focus-within:border-[#719294]">
            <span class="mr-2 mt-1">📝</span>
            <textarea
              v-model="form.comment_text"
              required
              placeholder="What was good? What could be improved?"
              class="w-full outline-none resize-none h-28 text-[#719294]"
            />
          </div>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="mt-2 bg-[#719294] text-white rounded-full py-2.5 font-semibold hover:opacity-90 active:scale-[0.98] transition"
        >
          Submit Review
        </button>

        <!-- Feedback -->
        <p
          v-if="message"
          class="text-sm text-center"
          :class="isError ? 'text-red-500' : 'text-green-600'"
        >
          {{ message }}
        </p>

      </form>
    </div>
  </div>
  </div>
</template>


<style scoped>  

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
